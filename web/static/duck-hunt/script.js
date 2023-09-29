var duck = document.getElementById("duck");
var dog = document.getElementById("dog");
var game = document.getElementById("game");
var duckTop = 0;
var duckSpeed = 30;
var duckLeft = -70;
var button = document.getElementById("myButton");
var points = 0;
var score = document.getElementById("score");

var duckFlyInterval = null;
var duckFallInterval = null;

var duckSound = new Audio('/static/duck-hunt/sounds/duck.mp3');
var duckShoot = new Audio('/static/duck-hunt/sounds/gunshot.mp3');
var reload = new Audio('/static/duck-hunt/sounds/reload.mp3');
var dogBark = new Audio('/static/duck-hunt/sounds/dog-bark.wav');

function startGame() {
    button.style.visibility = "hidden"
    startDuckFly();
    startDogWalk();
}


function startDogWalk() {
    var dogLeft = -110;

    dogGoRightInterval = setInterval(() => {
        dog.style.left = dogLeft + "px";
        dogLeft = dogLeft + 5;

        // check if the dog out of the screen
        if (dogLeft > game.offsetWidth) {
            dogLeft = -110;
        }
    }, 150);
}

function startDuckFly() {
    duck.src = "/static/duck-hunt/images/flyingduck.gif"
    duck.style.zIndex = 9;
    duckLeft = -70;

    // give random top value to the duck
    duckTop = Math.floor((Math.random() * 200) + 1);

    duckFlyInterval = setInterval(() => {
        duck.style.left = duckLeft + "px";
        duck.style.top = duckTop + "px";

        duckLeft += duckSpeed;

        duckLeft = duckLeft + 5;
        // check if the duck out of the screen
        if (duckLeft > game.offsetWidth) {
            duckLeft = -70;

            duckTop = Math.floor((Math.random() * 200) + 1);

            //  -2 point if duck is missed
            points -= 2;
            score.innerHTML = points;

        }

        // play the duck sound if left value of duck is between 240 - 290
        if (duckLeft > 240 && duckLeft < 290) {
            duckSound.play();
        }
    }, 150);
}


function shootDuck() {
    duck.src = '/static/duck-hunt/images/duckshot2.png';
    clearInterval(duckFlyInterval);
    shoot();
    var duckFall = 5;
    duck.style.zIndex = 0;
    setTimeout(() => {
        duck.src = '/static/duck-hunt/images/duckfalling.png'
        duckFallInterval = setInterval(() => {
            duckTop += duckFall;
            duck.style.top = duckTop + "px";

            duckFall += 3;

            //  check if duck is out of the screen
            if (duckTop > 700) {
                clearInterval(duckFallInterval);
                startDuckFly();
            }
        }, 150);
    }, 1000);

    // +1 point if duck is shot
    points += 1;
    score.innerHTML = points;

        // Отправляем AJAX-запрос для сохранения очков игры
        var csrfToken = $('meta[name="csrf-token"]').attr('content');
        if (userIsAuthenticated === true) {
            $.ajax({
            url: "http://127.0.0.1:8888/duck_hunt_save_points/" + points + "/",
            type: "POST",
            data: {
                csrfmiddlewaretoken: csrfToken,
            },
            success: function(data) {
                if (data.result === 'Success') {
                    console.log('Очки записаны в бд')
                } else {
                    alert("Ошибка при сохранении игры!");
                }
            },
            error: function() {
                alert("Произошла ошибка при выполнении запроса.");
            },
        });
        }


}


function shoot() {
    duckShoot.currentTime = 0;
    duckShoot.play();

}