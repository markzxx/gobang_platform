const app = require('http').createServer();
const io = require('socket.io')(app);

app.listen(3000);
console.log('This server is listening port: 3000');
let socketMaps = {};
let watchMaps = {};
let WatchingMaps = {};
let existUserNames = [];
io.on('connection', function (socket) {
    console.log('connect', socket.id);

    socket.on('watch', function (name) {
        if(WatchingMaps[socket.id])
            watchMaps[WatchingMaps[socket.id]] = watchMaps[WatchingMaps[socket.id]].filter(item => item !== socket.id);
        let users = watchMaps[name];
        if(users)
            users.push(socket.id);
        else
            users=[socket.id];
        watchMaps[name] = users;

        WatchingMaps[socket.id] = name;
        console.log(watchMaps);
    });

    socket.on('setName', function (name) {
        if(name == ""){
           let userName = createNewName();
            socketMaps[socket.id] = {
                name: userName,
                competitor: '',
                currentStep: false,
                isBlack: false
            };
            socket.emit('userName', userName);
            io.emit('allUsers', getAllUsers()); 
        }else{
            let user = socketMaps[socket.id];
            user.name = name;
            socketMaps[socket.id] = user;
            io.emit('allUsers', getAllUsers()); 
        }        
    });

    socket.on('applyGame', function (competitorId) {
        let applyId = socket.id;
        socketMaps[applyId].competitor = competitorId;
        socketMaps[competitorId].competitor = applyId;

        if (parseInt(Math.random() * 100 + 1, 10) % 2 === 0) {
            socketMaps[applyId].currentStep = true;
            socketMaps[applyId].isBlack = true;
        } else {
            socketMaps[competitorId].currentStep = true;
            socketMaps[competitorId].isBlack = true;
        }
        io.to(applyId).emit('beginGame', socketMaps[applyId]);
        io.to(competitorId).emit('beginGame', socketMaps[competitorId]);
        let gameInfo = {player1:socketMaps[applyId], player2:socketMaps[competitorId]};
        Notify(socketMaps[applyId], socketMaps[competitorId], 'beginGame', gameInfo);
        io.emit('allUsers', getAllUsers());
    });

    socket.on('step', function(stepInfo) {
        let competitorId = socketMaps[socket.id].competitor;
        let competitor = socketMaps[competitorId];
        competitor.currentStep = true;
        let info = {
            ownInfo: competitor,
            stepInfo: stepInfo
        };
        io.to(competitorId).emit('competitorStep', info);
        Notify(socketMaps[socket.id], competitor, 'step', info);
    });

    socket.on('disconnect', function () {
        console.log('disconnect');
        delete socketMaps[socket.id];
    });
});

// 新用户连接时随机生成新的用户名
function createNewName() {
    let newName = 'user' + parseInt(Math.random() * 10000 + 1, 10);
    while (existUserNames.includes(newName)) {
        newName = 'name' + parseInt(Math.random() * 10000 + 1, 10);
    }
    existUserNames.push(newName);
    return newName;
}

function getAllUsers() {
    let allUsers = [];
    for (let [key, value] of Object.entries(socketMaps)) {
        allUsers.push({
            id: key,
            ...value
        })
    }
    return allUsers;
}

function Notify(player1, player2, script, content) {
    if(watchMaps[player1.name]){
        watchMaps[player1.name].forEach(function(watcher){
            io.to(watcher).emit(script, content);
            console.log(watcher);
        }); 
    }
    if(watchMaps[player2.name]){
        watchMaps[player2.name].forEach(function(watcher){
            io.to(watcher).emit(script, content);
            console.log(watcher);
        }); 
    }
}