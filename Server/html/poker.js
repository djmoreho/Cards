src="jquery-1.11.3.min.js";
//url the ajax stuff posts to
var url ="127.0.0.01:8080/api?game=poker&action=";
//All the other stuff
var cardsPath = "card_pics/";
var playerHand = [];
var playerNumber;
var gameOver = false;
var currentPlayerTurn = 0;
var folded = false;
var pot = 0;
var loggedIn = false;
var ready = false;

function login(){
        var verb = "player_number";
        playerNumber=$.post(url + verb);
        
        playerHand.append(playerData[0][0]);
        playerHand.append(playerData[0][1]);
        $(".p3c1").attr('src',cardsPath + playerHand[0] + ".png");
        $(".p3c2").attr('src',cardsPath + playerHand[1] + ".png");
        loggedIn=true;
}

function fold(){
        //Check to see if it is the current player's turn
        if (currentPlayerTurn === playerNumber && !folded){
            var verb = "fold";
            $.post(url + verb);
            folded = true;
        }
}

function call(){
        var verb="call";
        $.post(url + verb);
        verb = "end_turn";
        $.post(url + verb);
}

function raise(raiseAmount){
        //Need an api call to check if its the player's turn.
        var verb = "bet&amount=" + str(raiseAmount); 
        $.post(url + verb);
        verb = "end_turn";
        $.post(url + verb);
}

function theGame(){
        loggedIn = login();
        
        while(!ready){
            ready = isReady();
        }
        
        //Need some way of getting player data.
        getPlayerData();u
        while(!gameOver){
            refresh();
            //wait a second
            wait(1000000);
        }
        gameover=false;
        reset();
}

function wait(timeToWait){
    var begin = new Date().getTime();
    var done = false;
    while(!done){
        if((new Date().getTime() - begin) > timeToWait){
            done = true;
        }
    }
}

//ignore for now
function reset(){
    login();
    $(".p1c1").attr('src',"playing-card-back.jpg");

    $(".p1c2").attr('src',"playing-card-back.jpg");

    $(".p2c1").attr('src',"playing-card-back.jpg");

    $(".p2c2").attr('src',"playing-card-back.jpg");

    $(".p3c1").attr('src',"playing-card-back.jpg");

    $(".p3c2").attr('src',"playing-card-back.jpg");

    $(".p4c1").attr('src',"playing-card-back.jpg");

    $(".p4c2").attr('src',"playing-card-back.jpg");
}

function refresh(){
    var verb = "river";
    river = $.post(url + verb);
    verb = "score";
    playerScores = $.post(url + verb);
	//quack
    pot = scoresJSON["Pot"];
    
    //Data for player's scores/Turn
    $("#p1-money").html("Player 1: " + playerScores[0].toString());
    $("#p2-money").html("Player 2: " + playerScores[1].toString());
    $("#p3-money").html("Player 3: " + playerScores[2].toString());
    $("#p4-money").html("Player 4: " + playerScores[3].toString());
    $("#playerMoney").html("Money Left: " + scoresJSON["playerScores"[playerNumber]].toString());
    $("#playerTurn").html("Player" + (scoresJSON["CurrentPlayerTurn"] + 1).toString() + "'s Turn" );
    
    //These ifs are for the river.
    
    if(river.length == 3){
        $(".center1").attr('src',cardsPath + river[0] + ".png");
        $(".center2").attr('src',cardsPath + river[1] + ".png");
        $(".center3").attr('src',cardsPath + river[2]+ ".png");
    }
    
    if(river.length == 4){
        $(".center4").attr('src',cardsPath + river[3] + ".png");
    }
    
    if(river.length == 5){
        $(".center5").attr('src',cardsPath + river[4] + ".png");
        gameOver = True;
    }
    
    
    //If the game is over, reveal all players hands
    if (gameOver) {
        //Get the hands of everyone
        hands = ScoresJSON["AllHands"];
        if(!hands.empty()){
            var users=[0,1,2,3];
            hands.remove(playerNumber);
            $(".p1c1").attr('src',cardsPath + hands[users[0]][0] + ".png");
            $(".p1c2").attr('src',cardsPath + hands[users[0]][1] + ".png");
            $(".p2c1").attr('src',cardsPath + hands[users[1]][0] + ".png");
            $(".p2c2").attr('src',cardsPath + hands[users[1]][1] + ".png");
            $(".p4c1").attr('src',cardsPath + hands[users[2]][0] + ".png");
            $(".p4c2").attr('src',cardsPath + hands[users[2]][1] + ".png");
        }
    }
}
