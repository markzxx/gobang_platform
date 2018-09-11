var CHESSBOARD_WIDTH = 450; // 棋盘大小
var CHESSBOARD_GRID = 30; // 棋盘每格大小
var CHESSBOARD_MARGIN = 15; // 棋盘内边距
var CHESS_SIZE = 0; // 棋盘格数
var IS_BLACK = true; // 是否黑棋
var IS_GAME_OVER = false; // 游戏是否结束
var IS_CAN_STEP = false; // 是否可以下棋（对手下棋时己方不能下棋）
var COMPETITOR_NAME = '';    // 对手的昵称

// 设置canvas的content的
var ctx = null;

var socket = io('http://10.20.13.19:8080');
// 棋盘坐标数组
var arrPieces = new Array();

$(document).ready(function () {
    clientSocket(socket);
    socket.emit('update_list', "update");
    bindPlayClick(socket);
    drawChessBoard();
});

// 画出棋盘
function drawChessBoard() {
    var canvas = document.getElementById('chessboard');
    canvas.width = CHESSBOARD_WIDTH;
    canvas.height = CHESSBOARD_WIDTH;
    ctx = canvas.getContext('2d');
    ctx.lineWidth = 1;
    CHESS_SIZE = Math.floor(CHESSBOARD_WIDTH / CHESSBOARD_GRID);

    for (var i = 0; i < CHESS_SIZE; i++) {
        ctx.strokeStyle = '#444';
        ctx.moveTo(CHESSBOARD_MARGIN + CHESSBOARD_GRID * i, CHESSBOARD_MARGIN);
        ctx.lineTo(CHESSBOARD_MARGIN + CHESSBOARD_GRID * i, CHESSBOARD_WIDTH - CHESSBOARD_MARGIN);
        ctx.stroke();
        ctx.moveTo(CHESSBOARD_MARGIN, CHESSBOARD_MARGIN + CHESSBOARD_GRID * i);
        ctx.lineTo(CHESSBOARD_WIDTH - CHESSBOARD_MARGIN, CHESSBOARD_MARGIN + CHESSBOARD_GRID * i);
        ctx.stroke();

        arrPieces[i] = new Array();
        for (var j = 0; j < CHESS_SIZE; j++) {
            arrPieces[i][j] = 0;
        }
    }
}

function drawNewPiece(i, j, isBlack) {
    var x = CHESSBOARD_MARGIN + i * CHESSBOARD_GRID + 1;
    var y = CHESSBOARD_MARGIN + j * CHESSBOARD_GRID + 1;
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
}


// 客户端socket
function clientSocket(socket) {
    socket.on('reply', function (data) {
        alert(data);
    });

    socket.on('update_list', function (userList) {
        handlebarsUserList(userList);
    });

    socket.on('push_game', function (gameInfo) {
        drawChessBoard();
        $.each(gameInfo.chess_log, function (index, value) {
            drawNewPiece(value[1], value[2], value[3]);
        });
        var status = 'Player  White：' + gameInfo.white +'\t\t\tBlack：' + gameInfo.black;
        $('#player-status').text(status);
        setGameStatus('Game Begin');
    });

    socket.on('go', function (info) {
        console.log(info);
        drawNewPiece(info[0], info[1], info[2]);
    });

    socket.on('finish', function (winner) {
        $('.play').text("Play");
        $('.play').removeAttr("disabled");
        if(winner==0)
            setGameStatus('Game draw!');
        else
            setGameStatus('Game finished, '+winner+' WIN！');
    });

    socket.on('error', function (info) {
        alert('游戏异常结束，'+info);
    });
}

function rd(n,m){
    var c = m-n+1;  
    return Math.floor(Math.random() * c + n);
}

// 绑定上分事件
function bindPlayClick(socket) {
    $('.play').click(function (e) {
        var $this = $(this);
        var status = $this.text();

        $this.text('Playing');
        $this.attr("disabled", "disabled");
        $(".user-status").attr("disabled", "disabled");
  
        watch($this.data('id'));
        socket.emit('play', {'sid':$this.data('id'), 'action':$this.attr("data-name")});
    });
/*
    $('.Go').click(function (e) {
        socket.emit('test_go', [$('#sid').data('id'), rd(1,15), rd(1,15), rd(0,1)]);
    });
    */
}

function watch(sid){
    $('.user-status').text('watch');
    $('.user-status').removeClass('gaming-status');
    $('#'+sid).addClass('gaming-status');
    $('#'+sid).text('watching');
    $('#watch_id').data('id', sid);
    socket.emit('watch', sid);
}

// 加载在线用户列表
function handlebarsUserList(userList) {
    var user_template = '<tr>'
                        +'<th>Sid</th>'
                        +'<th>Score</th>'
                        +'<th>Status</th>'
                        +'</tr>';
    $.each(userList, function (index, value) {
        user_template += '<tr><td><p class="user-id">'+value.sid+'</p></td>'
                    +'<td><p class="user-score">'+value.score+'</p></td>'
                    +'<td><button class="user-status" id="'+value.sid+'" >watch</button></td></tr>';
        
    });
    $('.player').html(user_template);
    $('.user-status').click(function (e) {
        watch($(this).attr('id'));
    });
    $('#'+$('#watch_id').data('id')).addClass('gaming-status');
    $('#'+$('#watch_id').data('id')).text('watching');
}

// 设置游戏状态
function setGameStatus(status) {
    $('#current_status').text(status);
}