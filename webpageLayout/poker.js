src="jquery-1.11.3.min.js";
//url the ajax stuff posts to
var url ="/api?game=poker&action=";
//All the other stuff
var cardsPath = "card_pics/";
var playerHand = playerData["playerHand"];
var playerNumber = playerData["playerNumber"];
var gameOver = false;
var currentPlayerTurn = 0;
var folded = false;
/*
 * Not Needed
 * 
var river1 = "BJ";
var river2 = "BJ";
var river3 = "BJ";
var river4 = "BJ";
var river5 = "BJ";
*/
var pot = 0;
var loggedIn = false;
var ready = false;

function login(){
        var verb = "add_player";
        $.post(url + verb);
        loggedIn=true;
}

//Not Sure What to do with this
function isReady(){
        var dataOut = {action:"IsItReady"};
        var redJSON=$.post(url + verb);
        return redJSON["Ready"];
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

function getPlayerData(){
        var dataOut={action:"GetPlayerData"};
        return $.post(url, dataOut, function(){},"json");
}

function theGame(){
        loggedIn = login();
        
        while(!ready){
            ready = isReady();
        }
        
        playerData = getPlayerData();
        playerHand = playerData["playerHand"];
        playerNumber = playerData["playerNumber"];
        while(!gameOver){
            refresh();
        }
}

function reset(){
    var playerData = $.post(url, {"datatype":"json", "headers":header});
    var playerHand = playerData["hand"];
    var pot = 0;
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
    playerScores = scoresJSON["Scores"];
    reveal = scoresJSON["allHands"];
    pot = scoresJSON["Pot"];
    gameOver = scoresJSON["GameOver"];
    
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
    }
    
    
    //If the game is over, reveal all players hands
    if (gameOver) {
        Hands = ScoresJSON["AllHands"];
        PlayerOneHand=[Hands.substr(0,2), Hands.substr(2,2)];
        PlayerTwoHand=[Hands.substr(4,2), Hands.substr(6,2)];
        PlayerThreeHand=[Hands.substr(8,2), Hands.substr(10,2)];
        PlayerFourHand=[Hands.substr(12,2), Hands.substr(14,2)]
        $(".p1c1").attr('src',cardsPath + playerOneHand[0] + ".png");

        $(".p1c2").attr('src',cardsPath + playerOneHand[1] + ".png");

        $(".p2c1").attr('src',cardsPath + playerTwoHand[0] + ".png");

        $(".p2c2").attr('src',cardsPath + playerTwoHand[1] + ".png");

        $(".p3c1").attr('src',cardsPath + playerThreeHand[0] + ".png");

        $(".p3c2").attr('src',cardsPath + playerThreeHand[1] + ".png");

        $(".p4c1").attr('src',cardsPath + playerFourHand[0] + ".png");

        $(".p4c2").attr('src',cardsPath + playerFourHand[1] + ".png");
        
        
    }
}

/*
if(playerNumber == 0){
    //var playerOneHand = //Get JSON for player one's hand.;
    $(".p1c1").attr('src',cardsPath + playerOne.cards[0] + ".png");
  
    $(".p1c2").attr('src',cardsPath + playerOne.cards[1] + ".png");
}

if(playerNumber == 1){
    //var playerTwoHand = //Get JSON for player two's hand.;
    $(".p2c1").attr('src',cardsPath + playerTwo.cards[0] + ".png");

    $(".p2c2").attr('src',cardsPath + playerTwo.cards[1] + ".png");
}

if(playerNumber == 2){
    //var playerThreeHand = //Get JSON for player three's hand.;
    $(".p3c1").attr('src',cardsPath + playerThree.cards[0] + ".png");

    $(".p3c2").attr('src',cardsPath + playerThree.cards[1] + ".png");
}

if(playerNumber == 3){
    //var playerFourHand = //Get JSON for player four's hand.;
    $(".p4c1").attr('src',cardsPath + playerFour.cards[0] + ".png");

    $(".p4c2").attr('src',cardsPath + playerFour.cards[1] + ".png");
}
*/
