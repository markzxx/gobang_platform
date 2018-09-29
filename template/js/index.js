var CHESSBOARD_WIDTH = 450; // 棋盘大小
var CHESSBOARD_GRID = 30; // 棋盘每格大小
var CHESSBOARD_MARGIN = 40; // 棋盘内边距
var CHESS_SIZE = 15; // 棋盘格数
var IS_BLACK = true; // 是否黑棋
var IS_GAME_OVER = false; // 游戏是否结束
var IS_CAN_STEP = false; // 是否可以下棋（对手下棋时己方不能下棋）
var range_max = 0;
// 设置canvas的content的
var ctx = null;

var socket = io('http://10.20.96.148:8080');
// var socket = io('http://10.20.106.72:8080');
// 棋盘坐标数组
var arrPieces = [];
var chess_log = null;

$(document).ready(function () {
    clientSocket(socket);
    socket.emit('update_list', "update");
    bindButtonClick(socket);
    drawChessBoard();
});

// 画出棋盘
function drawChessBoard() {
    var canvas = document.getElementById('chessboard');
    canvas.width = CHESSBOARD_WIDTH + 1 * CHESSBOARD_MARGIN;
    canvas.height = CHESSBOARD_WIDTH + 1 * CHESSBOARD_MARGIN;
    ctx = canvas.getContext('2d');
    ctx.lineWidth = 1;
    CHESS_SIZE = Math.floor(CHESSBOARD_WIDTH / CHESSBOARD_GRID);

    for (var i = 0; i < CHESS_SIZE; i++) {
        ctx.strokeStyle = '#444';
        ctx.font = "13px bold";
        ctx.fillText(i, CHESSBOARD_MARGIN + CHESSBOARD_GRID * i - 3, CHESSBOARD_MARGIN - 15);
        ctx.fillText(i, CHESSBOARD_MARGIN - 30, CHESSBOARD_MARGIN + CHESSBOARD_GRID * i + 4);
        ctx.moveTo(CHESSBOARD_MARGIN + CHESSBOARD_GRID * i, CHESSBOARD_MARGIN);
        ctx.lineTo(CHESSBOARD_MARGIN + CHESSBOARD_GRID * i, CHESSBOARD_WIDTH + CHESSBOARD_MARGIN - CHESSBOARD_GRID);
        ctx.stroke();
        ctx.moveTo(CHESSBOARD_MARGIN, CHESSBOARD_MARGIN + CHESSBOARD_GRID * i);
        ctx.lineTo(CHESSBOARD_WIDTH + CHESSBOARD_MARGIN - CHESSBOARD_GRID, CHESSBOARD_MARGIN + CHESSBOARD_GRID * i);
        ctx.stroke();
        arrPieces[i] = [];
        for (var j = 0; j < CHESS_SIZE; j++) {
            arrPieces[i][j] = 0;
        }
    }
}

// 画出棋子
function drawPiece(i, j) {
    // 当前游戏未结束且当前节点未落子
    if (IS_CAN_STEP && !IS_GAME_OVER && arrPieces[i][j] === 0) {
        // 画一个新棋子
        // drawNewPiece(i, j, IS_BLACK);
        color = IS_BLACK ? -1 : 1;
        // chess_log.push([i,j,color]);
        socket.emit('self_go', [$('#sid').data('id'), $('#chessboard').data('id'), i, j, color]);
    }
}

//画一个棋子
function drawNewPiece(i, j, isBlack) {
    var y = CHESSBOARD_MARGIN + i * CHESSBOARD_GRID + 1;
    var x = CHESSBOARD_MARGIN + j * CHESSBOARD_GRID + 1;
    ctx.beginPath();
    ctx.arc(x, y, Math.floor(CHESSBOARD_GRID / 2) - 2, 0, Math.PI * 2, true);
    ctx.closePath();
    var grd = ctx.createRadialGradient(x, y, Math.floor(CHESSBOARD_GRID / 3), x, y, Math.floor(CHESSBOARD_GRID / 10));
    if (isBlack) {
        grd.addColorStop(0, '#0A0A0A');
        grd.addColorStop(1, '#676767');
    } else {
        grd.addColorStop(0, '#D8D8D8');
        grd.addColorStop(1, '#F9F9F9');
    }
    ctx.fillStyle = grd;
    ctx.fill();

    // 记录坐标落子情况
    arrPieces[i][j] = isBlack ? -1 : 1;
}


// 客户端socket
function clientSocket(socket) {
    socket.on('reply', function (data) {
        console.log(data);
        alert(data);
    });

    socket.on('update_list', function (userList) {
        handlebarsUserList(userList);
    });

    socket.on('push_game', function (gameInfo) {
        drawChessBoard();

        chess_log = [];

        if (!gameInfo.chess_log) {
            $.each(gameInfo.chess_log, function (index, value) {
                // console.log(value);
                drawNewPiece(value[1], value[2], value[3] == -1);
                chess_log.push([value[1], value[2], value[3]]);
            });
        }

        $('#player-status1').text(gameInfo.white);
        $('#player-status2').text(gameInfo.black);
        if ('winner' in gameInfo) {
            $('#range').attr('max', chess_log.length);
            $('#range').val(chess_log.length);
            $('#range_num').val(chess_log.length);
            range_max = chess_log.length;
            if (gameInfo['winner'] == '0')
                setGameStatus('Game draw!');
            else
                setGameStatus('Game finished, ' + gameInfo['winner'] + ' WIN！');
        } else {
            setGameStatus('Game Begin');
            $('.record').attr("disabled", "disabled");
        }
    });

    socket.on('register', function (info) {
        $(".user-status").removeAttr("disabled");
    });

    socket.on('go', function (info) {
        // console.log(info);
        drawNewPiece(info[0], info[1], info[2] == -1);
        chess_log.push(info);
        IS_CAN_STEP = !IS_CAN_STEP;
    });

    socket.on('finish', function (winner) {
        $('#range').attr('max', chess_log.length);
        $('#range').val(chess_log.length);
        $('#range_num').val(chess_log.length);
        range_max = chess_log.length;
        if (winner == 0)
            setGameStatus('Game draw!');
        else
            setGameStatus('Game finished, ' + winner + ' WIN！');
        stopSelfPlay();
    });

    socket.on('error_finish', function (winner) {
        drawChessBoard();
        setGameStatus('Game error finished!');
        stopSelfPlay();
    });

    socket.on('error', function (info) {
        if (info.type == 1) {
            $("#info-modal-box-msg").html("<p>Error, " + info.info + "</p><button type=\"button\" id=\"error_finish\">Click here to force finish.</button>");
            $('#error_finish').click(function () {
                socket.emit('error_finish', getinfo());
                $("#info-modal-box").modal("hide");
            });
            $("#info-modal-box").modal("show");
        } else if (info.type == 2) {
            $("#info-modal-box-msg").html("<p>游戏异常结束," + info.info + "</p>");
            $("#info-modal-box").modal("show");
        } else if (info.type == 3) {
            $("#info-modal-box-msg").html("<p>" + info.info + "</p>");
            $("#info-modal-box").modal("show");
        }
        // alert('游戏异常结束，'+info);
    });
}

function rd(n, m) {
    var c = m - n + 1;
    return Math.floor(Math.random() * c + n);
}

function getinfo() {
    return {'player': $('#sid').data('id'), 'tag': $('#chessboard').data('id')};
}

function stopSelfPlay() {
    $('#self_play').data('name', 'play');
    switchStatus($('.user-status'), 'play', 'gaming-status');
    // $('#player-status1').text("");
    // $('#player-status2').text("");
    $('#play').removeAttr("disabled");
    $('.record').removeAttr("disabled");
    IS_CAN_STEP = false;
}


function playWith(sid) {
    // $('.user-status').removeClass('label_active');
    var bnt = $('#' + sid);
    var all_bnt = $(".user-status");
    var player = $('#sid').data('id');
    var tag = $('#chessboard').data('id');
    // bnt.addClass('gaming-status');
    // bnt.addClass('label_active');
    if (bnt.text() == 'play') {
        switchStatus(all_bnt, 'play', 'gaming-status');
        switchStatus(bnt, 'stop', 'gaming-stop');
        all_bnt.attr("disabled", "disabled");
        IS_BLACK = tag > 0;
        if (IS_BLACK)
            IS_CAN_STEP = true;
        socket.emit('self_play', {'player': player, 'AI': sid, 'tag': tag});
    } else {
        socket.emit('error_finish', getinfo());
    }
}

function watch() {
    // $('.user-status').text('watch');
    // $('.user-status').removeClass('gaming-status');
    // $('.user-status').removeClass('label_active');
    // $('#' + sid).addClass('gaming-status');
    // $('#' + sid).addClass('label_active');
    $('#watch_id').data('id', sid);
    socket.emit('watch', getinfo());
}

// 绑定各种按键
function bindButtonClick(socket) {
    //绑定棋盘落子
    $('#chessboard').click(function (e) {
        var y = Math.round((e.offsetX - CHESSBOARD_MARGIN) / CHESSBOARD_GRID);
        var x = Math.round((e.offsetY - CHESSBOARD_MARGIN) / CHESSBOARD_GRID);
        drawPiece(x, y);
    });

    //动态设置ranklist高度
    // $(".rank_list").css("top",$(".play_chess").offset().top+"px");

    //切换棋盘
    $('.tag').click(function () {
        $('#chessboard').data('id', $(this).data('id'));
        watch();
    });

    //开始比赛
    $('#play').click(function () {
        stopSelfPlay();
        $(this).attr("disabled", "disabled");
        $('.record').attr("disabled", "disabled");
        $(".user-status").attr("disabled", "disabled");
        var player = $('#sid').data('id');
        socket.emit('play', {'player': player, 'tag': 1});
        for (var i = 0; i < 1000; i++) ;
        socket.emit('play', {'player': player, 'tag': -1});
    });

    //开始人机对战
    // $('#self_play').click(function () {
    //     var $this = $(this);
    //     var status = $this.data('name');
    //     var player = $this.data('id');
    //     var tag = $('#chessboard').data('id');
    //     if (status == 'play') {
    //         $this.data('name', 'stop');
    //         $this.text('Stop');
    //         IS_BLACK = tag > 0;
    //         if (IS_BLACK)
    //             IS_CAN_STEP = true;
    //         socket.emit('self_play', {'player': player, 'AI': player, 'tag': tag});
    //     } else {
    //         socket.emit('error_finish', getinfo());
    //     }
    // });

    //复盘系统
    $("#range_num").change(function (event) {
        var num = parseInt($("#range_num").val());
        if (num <= range_max && num >= 0) {
            $('#range').val(num).change();
        }
    });

    $("#start").click(function () {
        $('#range_num').val(0).change();
        $('#range').val(0).change();
    });

    $('#left').click(function () {
        if (parseInt($('#range_num').val()) - 1 >= 0) {
            $('#range_num').val(parseInt($('#range_num').val()) - 1);
            $('#range').val(parseInt($('#range_num').val())).change();
        }
    });

    $('#right').click(function () {
        if (parseInt($('#range_num').val()) + 1 <= range_max) {
            $('#range_num').val(parseInt($('#range_num').val()) + 1);
            $('#range').val(parseInt($('#range_num').val())).change();
        }
    });

    $('#big-right').click(function () {
        if (parseInt($('#range').val()) + 5 <= range_max) {
            $('#range_num').val(parseInt($('#range').val()) + 5).change();
        } else {
            $('#range_num').val(range_max).change();
        }
        $('#range').val(parseInt($('#range').val()) * 1 + 5).change();
    });
    $('#big-left').click(function () {
        if (parseInt($('#range').val()) - 5 >= 0) {
            $('#range_num').val(parseInt($('#range').val()) - 5).change();
        } else {
            $('#range_num').val(0).change();
        }
        $('#range').val(parseInt($('#range').val()) - 5).change();
    });
    $("#end").click(function (event) {
        $('#range_num').val(range_max).change();
        $('#range').val(range_max).change();
    });

    $('#range').change(function () {
        drawChessBoard();
        for (var i = 0; i < parseInt($('#range').val()); i++)
            drawNewPiece(chess_log[i][0], chess_log[i][1], chess_log[i][2] == -1);
    });

    $('#download').click(function () {
        try {
            $("#info-modal-box-msg").html("<p>Download Successfully</p>");
            var aTag = document.createElement('a');
            var blob = new Blob([chess_log.join('\n')]);
            aTag.download = "chess_log.txt";
            aTag.href = URL.createObjectURL(blob);
            aTag.click();
            URL.revokeObjectURL(blob);
        } catch (err) {
            $("#info-modal-box-msg").html("<p>Some errors happened. Please make sure you have played a game.</p>");
        }
    });
}

function switchStatus(bnt, text, status) {
    bnt.removeClass('gaming-status');
    bnt.removeClass('gaming-stop');
    bnt.addClass(status);
    bnt.text(text);
}


// RankList分页实现
// function change_page(id) {
//   Page.now_page = id;
//   Page.page_html = "";
//   var user_rank_html = '<tr class="warning"><th colspan=4 style="text-align:center;cursor:move">RankList</th></tr><tr class="active"><th>#</th>' + '<th width="25%">Sid</th>' + '<th>Score</th>' + '<th>Status</th></tr>';
//   let page_active = "";
//   for (var i = 0; i < Page.page_num; i++) {
//     if (i == Page.now_page) {
//       page_active = "page_active";
//     } else {
//       page_active = "";
//     }
//     Page.page_html += "<button class='btn btn-default btn-sm " + page_active + "' onclick='change_page(" + i + ")'>" + (parseInt(i) + 1) + "</button>";
//   }
//   for (var index = Page.now_page * Page.each_num; index < (((Page.now_page + 1) * Page.each_num) > Page.items_num ? Page.items_num : (Page.now_page + 1) * Page.each_num); index++) {
//     user_rank_html += Page.items[index];
//   }
//   user_rank_html += "<tr class='active' id='page_box' style='text-align:center;'><td colspan='4'>" +
//     // "<button class='btn btn-info btn-sm' id='page-left'><i class='glyphicon glyphicon-arrow-left'></i></button>"+
//     Page.page_html +
//     // "<button class='btn btn-info btn-sm' id='page-right'><i class='glyphicon glyphicon-arrow-right'></i></button>"+
//     "</td></tr>";
//   $('#rank_table').html(user_rank_html);
//   $('.user-status').click(function(e) {
//     watch($(this).attr('id'));
//   });
//   $('#' + $('#watch_id').data('id')).addClass('gaming-status');
// }
// // 加载在线用户列表
// function handlebarsUserList(userList) {
//   console.log(userList);
//   // let str_text='[';
//   // for (var i = 0; i < userList.length; i++) {
//   //   str_text+=JSON.stringify(userList[i])+",";
//   // }
//   // str_text=str_text.substring(0,str_text.length-1);
//   // str_text+="]";
//   // console.log(str_text);
//   var now_sid = parseInt($("#sid").attr("data-id"));
//   var user_rank_html = '<tr class="warning"><th colspan=4 style="text-align:center;cursor:move">RankList</th></tr><tr class="active"><th>#</th>' + '<th width="25%">Sid</th>' + '<th>Score</th>' + '<th>Status</th></tr>';
//   let state = "active";
//   //pages分页
//   Page.items_num = userList.length;
//   Page.page_num = Math.ceil(Page.items_num / Page.each_num);
//   Page.items = [];
//   Page.now_page = 0; //Where are you,default 0.
//   Page.page_html = "";
//   let value;
//   for (var i = 0; i < Page.page_num; i++) {
//     for (var index = i * Page.each_num; index < (((i + 1) * Page.each_num) > Page.items_num ? Page.items_num : (i + 1) * Page.each_num); index++) {
//       value = userList[index];
//       // if(index%2==0)state="active";
//       // if(index%2!=0)state="";
//       if (parseInt(value.sid) == parseInt(now_sid)) {
//         "success";
//         Page.now_page = i;
//       }
//       Page.items.push('<tr class="' + state + '"><td>' + (index + 1) + '</td><td><p class="user-id">' + value.sid + '</p></td>' + '<td><p class="user-score">' + value.score + '</p></td>' + '<td><button class="label user-status" id="' + value.sid + '" >watch</button></td></tr>')
//     }
//   }
//
//   let page_active = "";
//   for (var i = 0; i < Page.page_num; i++) {
//     if (i == Page.now_page) {
//       page_active = "page_active";
//     } else {
//       page_active = "";
//     }
//     Page.page_html += "<button class='btn btn-default btn-sm " + page_active + "' onclick='change_page(" + i + ")'>" + (parseInt(i) + 1) + "</button>";
//   }
//
//   //Default : show page which in you are.log((((i+1)*Page.each_num)>Page.items_num?Page.items_num:(i+1)*Page.each_num))
//   for (var index = Page.now_page * Page.each_num; index < (((Page.now_page + 1) * Page.each_num) > Page.items_num ? Page.items_num : (Page.now_page + 1) * Page.each_num); index++) {
//     user_rank_html += Page.items[index];
//   }
//   user_rank_html += "<tr class='active' id='page_box' style='text-align:center;'><td colspan='4'>" +
//     // "<button class='btn btn-info btn-sm' id='page-left'><i class='glyphicon glyphicon-arrow-left'></i></button>"+
//     Page.page_html +
//     // "<button class='btn btn-info btn-sm' id='page-right'><i class='glyphicon glyphicon-arrow-right'></i></button>"+
//     "</td></tr>";
//   $('#rank_table').html(user_rank_html);
//   $('.user-status').click(function(e) {
//     watch($(this).attr('id'));
//   });
//   $('#' + $('#watch_id').data('id')).addClass('gaming-status');
//
// }
// 加载在线用户列表(无分页)
function handlebarsUserList(userList) {
    console.log(userList);
    var now_sid = parseInt($("#sid").attr("data-id"));
    var now_rank = 11;
    var now_score = 0;
    var user_rank_html = '<tr><th colspan=4 style="text-align:center;cursor:default">RankList</th></tr><tr class="active"><th>#</th>' + '<th width="25%">Sid</th>' + '<th>Score</th>' + '<th>Status</th></tr>';
    var state = "";

    var value;
    for (var index = 0; index < userList.length; index++) {
        value = userList[index];
        if (index < 10) {
            if (now_sid == value.sid) {
                state = "info";
                now_rank = index + 1;
                now_score = value.score;
            }
            user_rank_html += '<tr class="' + state + ' rank-' + (index + 1) + '"><td><p class="user-rank">' + (index + 1) + '</p></td><td><p class="user-id">' + value.sid + '</p></td>' + '<td><p class="user-score">' + value.score + '</p></td>' + '<td><button class="label user-status" id="' + value.sid + '" >play</button></td></tr>';
            state = "";
        } else {
            if (now_sid == value.sid) {
                now_rank = index + 1;
                now_score = value.score;
                break;
            }
        }
    }
    if (parseInt(now_rank) > 10) {
        user_rank_html += "<tr class='active' id='page_box' style='text-align:center;'>" +
            '<tr class="info"><td>' + (now_rank) + '</td><td><p class="user-id">' + now_sid + '</p></td>' + '<td><p class="user-score">' + now_score + '</p></td><td>Yourself</td>' + '</tr>' +
            "</tr>";
    }

    $('#rank_table').html(user_rank_html);
    $('.user-status').click(function (e) {
        playWith($(this).attr('id'));
    });
    $('.user-status').addClass('gaming-status');
    watch();
}

// 设置游戏状态
function setGameStatus(status) {
    $('#current_status').html("&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;" + status);
}

//设置ranklist可拖动
var Dragging = function (validateHandler) {
    //参数为验证点击区域是否为可移动区域，如果是返回欲移动元素，负责返回null
    var draggingObj = null; //dragging Dialog
    var diffX = 0;
    var diffY = 0;

    function mouseHandler(e) {
        switch (e.type) {
            case 'mousedown':
                draggingObj = validateHandler(e); //验证是否为可点击移动区域
                if (draggingObj != null) {
                    diffX = e.clientX - draggingObj.offsetLeft;
                    diffY = e.clientY - draggingObj.offsetTop;
                }
                break;
            case 'mousemove':
                if (draggingObj) {
                    draggingObj.style.left = (e.clientX - diffX) + 'px';
                    draggingObj.style.top = (e.clientY - diffY) + 'px';
                }
                break;
            case 'mouseup':
                draggingObj = null;
                diffX = 0;
                diffY = 0;
                break;
            case "touchstart":
                draggingObj = validateHandler(e); //验证是否为可点击移动区域

                if (draggingObj != null) {
                    // console.dir(e);
                    // console.log(e["touches"][0]["clientX"],e["touches"][0]["clientY"]);
                    // console.log(draggingObj.offsetLeft,draggingObj.offsetTop);
                    diffX = e["touches"][0]["clientX"] - draggingObj.offsetLeft;
                    diffY = e["touches"][0]["clientY"] - draggingObj.offsetTop;
                }

                break;
            case 'touchmove':
                if (draggingObj) {
                    draggingObj.style.left = (e["touches"][0]["clientX"] - diffX) + 'px';
                    draggingObj.style.top = (e["touches"][0]["clientY"] - diffY) + 'px';
                }
                break;
            case 'touchend':
                draggingObj = null;
                diffX = 0;
                diffY = 0;
                break;
        }
    }

    return {
        enable: function () {
            document.addEventListener('mousedown', mouseHandler);
            document.addEventListener('mousemove', mouseHandler);
            document.addEventListener('mouseup', mouseHandler);
            document.addEventListener('touchmove', mouseHandler);
            document.addEventListener('touchstart', mouseHandler);
            document.addEventListener('touchend', mouseHandler);
        },
        disable: function () {
            document.removeEventListener('mousedown', mouseHandler);
            document.removeEventListener('mousemove', mouseHandler);
            document.removeEventListener('mouseup', mouseHandler);
            document.removeEventListener('touchmove', mouseHandler);
            document.removeEventListener('touchstart', mouseHandler);
            document.removeEventListener('touchend', mouseHandler);
        }
    }
};

function getDraggingDialog(e) {
    var target = e.target;
    while (target && target.className.indexOf('dialog-title') == -1) {
        target = target.offsetParent;
    }
    if (target != null) {
        return target.offsetParent;
    } else {
        return null;
    }
}


Dragging(getDraggingDialog).enable();
