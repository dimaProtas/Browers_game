document.addEventListener('DOMContentLoaded', function () {
        var socketHost = $('meta[name="socket-host"]').attr('content');
        // JavaScript-код для отправки сообщения через WebSocket
        const socket = new WebSocket(socketHost + 'ws/messages/');

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
            // Обработка полученного сообщения, например, вывод на экран
            //const isSentByMe = data.isSentByMe;
            addMessage(data.sender, data.message, data.timestamp);
        };


        // Обработчик события submit формы
        document.querySelector('.message-form').addEventListener('submit', function (event) {
            event.preventDefault(); // Предотвращаем стандартное действие формы (перенаправление)

            const messageInput = document.getElementById('message-input');
            const message = messageInput.value;


            // Проверяем, не является ли сообщение пустым
            if (message.trim() !== '' & userIsAuthenticated === true) {
                socket.send(JSON.stringify({ message }));
                messageInput.value = '';
            } else if (userIsAuthenticated === false) {
                $("#confirmModal").modal("show");
            }
        });

            const messageContainer = document.querySelector('.message-container');
            let isScrolledToBottom = true;

            // Обработчик прокрутки контейнера
            messageContainer.addEventListener('scroll', function () {
                // Проверяем, находится ли скролл внизу
                isScrolledToBottom = messageContainer.scrollHeight - messageContainer.scrollTop === messageContainer.clientHeight;
            });

            function addMessage(sender, message, timestamp) {
                const messageDiv = document.createElement('div');
                messageDiv.className = 'message';

                const senderTimestampDiv = document.createElement('div');

                const senderSpan = document.createElement('span');
                senderSpan.className = 'sender';
                senderSpan.textContent = sender;

                const timestampSpan = document.createElement('span');
                timestampSpan.className = 'timestamp';
                timestampSpan.textContent = timestamp;

                senderTimestampDiv.appendChild(senderSpan);
                senderTimestampDiv.appendChild(timestampSpan);

                const messageTextSpan = document.createElement('span');
                messageTextSpan.className = 'message-text';
                messageTextSpan.textContent = message;

                messageDiv.appendChild(senderTimestampDiv);
                messageDiv.appendChild(messageTextSpan);

                messageContainer.appendChild(messageDiv); // Добавляем сообщение в конец контейнера

                var currentUser = document.getElementById('user-data').getAttribute('data-current-user');


                // Помечаем сообщение, если оно отправлено мной
                if (sender === currentUser) {
                        messageDiv.classList.add('sent-by-me'); // Добавляем класс CSS для пометки

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


                // Если скролл находится внизу, автоматически прокручиваем
                if (isScrolledToBottom) {
                    messageContainer.scrollTop = messageContainer.scrollHeight;
                }
            }

            window.addEventListener('load', function () {
            // Получаем контейнер сообщений
            const messageContainer = document.querySelector('.message-container');

            // Устанавливаем положение скролла внизу
            messageContainer.scrollTop = messageContainer.scrollHeight;
        });
    });