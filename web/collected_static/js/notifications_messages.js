document.addEventListener('DOMContentLoaded', function () {

        var socketHost = $('meta[name="socket-host"]').attr('content');
        var currentUserID = document.getElementById('user-data-id').getAttribute('data-current-user-id');

        const socket = new WebSocket(socketHost + 'ws/notifications_messages/');

        let notificationTimeout; // таймаут для авто закрытия уведомления


        $("#confirmModalmessage").hide();

        socket.onopen = function (e) {
            console.log('WebSocket connection established.');
        };

        socket.onclose = function (event) {
            if (event.wasClean) {
                console.log(`Closed cleanly, code=${event.code}, reason=${event.reason}`);
            } else {
                console.error('Connection died');
            }
        };

        socket.onmessage = function(event) {
            const data = JSON.parse(event.data);
            console.log('Текущий пользователь:', currentUserID, 'Сообщение:', data.message, 'Отправитель:', data.sender);
            // Проверяем, отправлено ли сообщение (текущему пользователю)
            if (data.recipient_id == currentUserID) {
                addMessage(data.sender, data.message, data.timestamp);
            };
        };


        function addMessage(sender, message, timestamp) {
            const messageDiv = document.createElement('div');
            messageDiv.className = 'message-item-notification';

            const senderStrong = document.createElement('strong');
            senderStrong.textContent = sender;

            const messageParagraph = document.createElement('p');
            messageParagraph.textContent = message;

            const timestampSmall = document.createElement('small');
            timestampSmall.textContent = timestamp;

            const closeButton = document.createElement('button');
            closeButton.type = 'button';
            closeButton.className = 'close';
            closeButton.innerHTML = '&times;';
            closeButton.addEventListener('click', function() {
                messageDiv.style.display = 'none'; // Скрыть уведомление при закрытии
            });

            //Добавление ссылки на уведомление
            // const messageLink = document.createElement('a');
            // messageLink.href = "/private_message/";
            // messageLink.appendChild(messageDiv);

            // Добавляем созданные элементы внутрь messageDiv
            messageDiv.appendChild(senderStrong);
            messageDiv.appendChild(closeButton);
            messageDiv.appendChild(messageParagraph);
            messageDiv.appendChild(timestampSmall);

            // Добавляем messageDiv в контейнер .notification-container
            const notificationContainer = document.querySelector('.notification-container');
            notificationContainer.appendChild(messageDiv);

            // Задержка перед началом анимации
            setTimeout(() => {
                messageDiv.style.opacity = '1'; // Сделать уведомление видимым
            }, 10);

            // Закрыть уведомление через некоторое время (например, 5 секунд)
            notificationTimeout = setTimeout(() => {
                messageDiv.style.opacity = '0'; // Сделать уведомление невидимым
                setTimeout(() => {
                    notificationContainer.removeChild(messageDiv); // Удалить уведомление
                }, 500); // После анимации исчезновения
            }, 5000); // 5 секунд задержки

            var currentUser = document.getElementById('user-data').getAttribute('data-current-user');


            // Помечаем сообщение, если оно отправлено не мной
            if (sender !== currentUser) {
                    // Воспроизводим звук полученого сообщения
                    // const messageSound = document.getElementById('messageSoundAdd');
                    // messageSound.play();
                }

            $(".close").click(function() {
                console.log('Закрыть окно!!!');
                // Удаляем класс "opened" для скрытия модального окна
                $("#confirmModalmessage").hide();
                $(".modal-body-message").empty();
            });

        };
});

