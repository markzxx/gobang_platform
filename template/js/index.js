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
    socket.emit('watch', $("#sid").data('id'));
    bindPlayClick(socket);
    bindApplyGameClick(socket);
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

// 点击棋盘进行落子
function chessClick() {
    $('#chessboard').click(function (e) {
        var x = Math.floor(e.offsetX / CHESSBOARD_GRID);
        var y = Math.floor(e.offsetY / CHESSBOARD_GRID);
        drawPiece(x, y);
    })
}

// 检查棋牌中是否还存在空位
function checkIsExistEmpty() {
    var isExistEmpty = false;
    for (var i = 0; i < CHESS_SIZE; i++) {
        for (var j = 0; j < CHESS_SIZE; j++) {
            if (arrPieces[i][j] === 0) {
                isExistEmpty = true;
                break;
            }
        }
    }
    if (!isExistEmpty) {
        setTimeout(function () {
            alert('平局!')
        }, 0);
    }
}
// 落下棋子后检查是否赢得比赛
function doCheck(x, y) {
    horizontalCheck(x, y);
    verticalCheck(x, y);
    downObliqueCheck(x, y);
    upObliqueCheck(x, y);
}

// 游戏结束
function isOver(x, y, sum) {
    if (sum === 5) {
        IS_GAME_OVER = true;
        setTimeout(function () {
            alert('Game Over!')
        }, 0);
    }
}

// 横轴方向检测
function horizontalCheck(x, y) {
    var sum = -1;

    for (var i = x; i >= 0; i--) {
        if (arrPieces[i][y] === arrPieces[x][y]) {
            sum++;
        } else {
            i = -1;
            break;
        }
    }
    for (var i = x; i < CHESS_SIZE; i++) {
        if (arrPieces[i][y] === arrPieces[x][y]) {
            sum++;
        } else {
            i = CHESS_SIZE;
            break;
        }
    }
    isOver(x, y, sum);
}

// 竖轴方向检测
function verticalCheck(x, y) {
    var sum = -1;

    for (var j = y; j >= 0; j--) {
        if (arrPieces[x][j] === arrPieces[x][y]) {
            sum++;
        } else {
            j = -1;
            break;
        }
    }
    for (var j = y; j < CHESS_SIZE; j++) {
        if (arrPieces[x][j] === arrPieces[x][y]) {
            sum++;
        } else {
            j = CHESS_SIZE;
            break;
        }
    }
    isOver(x, y, sum);
}

// 下斜方向检测
function downObliqueCheck(x, y) {
    var sum = -1;

    for (var i = x, j = y; i >= 0 && y >= 0;) {
        if (arrPieces[i][j] === arrPieces[x][y]) {
            sum++;
        } else {
            j = i = -1;
            break;
        }
        i--;
        j--;
    }
    for (var i = x, j = y; i < CHESS_SIZE && j < CHESS_SIZE;) {
        if (arrPieces[i][j] === arrPieces[x][y]) {
            sum++;
        } else {
            j = i = CHESS_SIZE;
            break;
        }
        i++;
        j++;
    }
    isOver(x, y, sum);
}

// 上斜方向检测
function upObliqueCheck(x, y) {
    var sum = -1;

    for (var i = x, j = y; i >= 0 && j < CHESS_SIZE;) {
        if (arrPieces[i][j] === arrPieces[x][y]) {
            sum++;
        } else {
            j = CHESS_SIZE;
            i = -1;
            break;
        }
        i--;
        j++;
    }
    for (var i = x, j = y; i < CHESS_SIZE && j >= 0;) {
        if (arrPieces[i][j] === arrPieces[x][y]) {
            sum++;
        } else {
            i = CHESS_SIZE;
            j = -1;
            break;
        }
        i++;
        j--;
    }
    isOver(x, y, sum);
}

// 客户端socket
function clientSocket(socket) {
    socket.on('reply', function (data) {
        alert(data);
    });

    socket.on('update_list', function (userList) {
        console.log(userList);
        handlebarsUserList(userList, socket.id, socket);
    });

    socket.on('push_game', function (gameInfo) {
        drawChessBoard();
        console.log(gameInfo);
        $.each(gameInfo.chess_log, function (index, value) {
            drawNewPiece(value[1], value[2], value[3]);
        });
        var status = 'Player: White：' + gameInfo.white +'\t\t\tBlack：' + gameInfo.black;
        $('#player-status').text(status);
        setGameStatus('Game Begin');
    });

    socket.on('go', function (info) {
        console.log(info);
        drawNewPiece(info[0], info[1], info[2]);
    });

    socket.on('finish', function (winner) {
        if(winner==0)
            setGameStatus('平局');
        else
            setGameStatus('游戏结束，'+winner+'获胜！');
    });

    socket.on('error', function (info) {
        alert('游戏异常结束，'+info);
    });

    socket.on('competitorStep', function (info) {
        var ownInfo = info.ownInfo,
            stepInfo = info.stepInfo;

        IS_CAN_STEP = ownInfo.currentStep;
        drawNewPiece(stepInfo.x, stepInfo.y, !ownInfo.isBlack);
        IS_GAME_OVER = stepInfo.isGameOver;
        var status = '';
        if(IS_GAME_OVER) {
            satus = '游戏结束了。';
        } else {
            if(IS_CAN_STEP) {
                status = '该我下棋了...';
            } else {
                status = '等待 ' + COMPETITOR_NAME + ' 下棋中...';
            }
        }
        setGameStatus(status);
        
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
/*      if (status == 'Play'){
            $this.text('Stop');
            $(this).attr("data-name", "play");
        }else{
            $this.text('Play');
            $(this).attr("data-name", "stop");
        }
  */
        socket.emit('play', {'sid':$this.data('id'), 'action':$this.attr("data-name")});
    });

    $('.Go').click(function (e) {
        socket.emit('go', [456, 789, rd(1,15), rd(1,15), rd(0,1)]);
    });
}

// 绑定申请对战事件
function bindApplyGameClick(socket) {
    $('.user-status').click(function (e) {
        var $this = $(this);
        socket.emit('watch', $this.data('id'));
    });
}

// 加载在线用户列表
function handlebarsUserList(userList, ownId, socket) {
    var user_template = '<tr>'
                        +'<th>Sid</th>'
                        +'<th>Score</th>'
                        +'<th>Status</th>'
                        +'</tr>';
    $.each(userList, function (index, value) {
        user_template += '<tr><td><p class="user-id">'+value.sid+'</p></td>'
                    +'<td><p class="user-score">'+value.score+'</p></td>'
                    +'<td><button class="user-status ready" data-id="'+value.sid+'" >ready</button></td></tr>';
        
    });
    $('.player').html(user_template);
    bindApplyGameClick(socket);
}

// 下棋触发socket
function stepPiece(x, y, isGameOver) {
    IS_CAN_STEP = false;
    var status = '等待 ' + COMPETITOR_NAME + ' 下棋中...';
    if(isGameOver) {
        status = '游戏结束.'
    }
    setGameStatus(status);
    socket.emit('step', {
        x: x,
        y: y,
        isGameOver: isGameOver
    });
}

// 设置游戏状态
function setGameStatus(status) {
    $('#current_status').text(status);
}