document.addEventListener('DOMContentLoaded', function () {

        var socketHost = $('meta[name="socket-host"]').attr('content');
        var currentUserID = document.getElementById('user-data-id').getAttribute('data-current-user-id');

        const socket = new WebSocket(socketHost + 'ws/private_messages/');

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
//            console.log('Текущий пользователь:', currentUserID, 'Получатель:', data.recipient_id, 'Отправитель:', data.sender_id);
            // Проверяем, отправлено ли сообщение (текущему пользователю)
            if (data.recipient_id == currentUserID || data.sender_id == currentUserID) {
                addMessage(data.sender, data.message, data.timestamp);
            };
        };

        $(document).ready(function() {
            // Получите элементы формы и кнопки отправки
            var messageInput = $("#message-input");
            var sendButton = $("#send-button");
            var recipientId = null;

            // Обработчик клика на кнопке отправки
            sendButton.click(function() {
                // Получить текст сообщения из поля ввода
                var message = messageInput.val();

                // Проверка на наличие текста в сообщении
                if (message.trim() !== "" && recipientId !== null) {
                    // Отправить сообщение на сервер WebSocket
                    socket.send(JSON.stringify({ message, recipientId }));
                    // Очистить поле для ввода
                    messageInput.val("");
                }
            });

                // Делегирование событий для элементов .friend
                $(".private_message").on("click", ".friend", function() {
                    recipientId = $(this).data("user-id"); // Установите recipientId при клике на друга

                    // Уберает класс "selected" у всех других элементов с классом "friend"
                    $(".friend").removeClass("selected");

                    // Добавьте класс "selected" к текущему элементу
                    $(this).addClass("selected");
                });
            });

            const messageContainer = document.querySelector('.message-container');
            let isScrolledToBottom = true;

            function addMessage(sender, message, timestamp) {
                const messageDiv = document.createElement('div');
                messageDiv.className = 'message-item';

                const senderStrong = document.createElement('strong');
                senderStrong.textContent = sender;

                const messageParagraph = document.createElement('p');
                messageParagraph.textContent = message;

                const timestampSmall = document.createElement('small');
                timestampSmall.textContent = timestamp;

                // Добавляем созданные элементы внутрь messageDiv
                messageDiv.appendChild(senderStrong);
                messageDiv.appendChild(messageParagraph);
                messageDiv.appendChild(timestampSmall);

                // Добавляем messageDiv в div '.message_block_container'
                const messageContainer = document.querySelector('.message_block_container');
                messageContainer.appendChild(messageDiv);

                var currentUser = document.getElementById('user-data').getAttribute('data-current-user');

                // Помечаем сообщение, если оно отправлено мной
                if (sender === currentUser) {
                        messageDiv.classList.add('sender'); // Добавляем класс CSS для пометки

                        // Воспроизводим звук отправки сообщения
                        const messageSound = document.getElementById('messageSound');
                        messageSound.play();
                    }

                // Помечаем сообщение, если оно отправлено не мной
                if (sender !== currentUser) {
                        // Воспроизводим звук полученого сообщения
                        const messageSound = document.getElementById('messageSoundAdd');
                        messageSound.play();
                    }
            }

});
