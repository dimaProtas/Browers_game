$(document).ready(function() {
    var messageHistory = [];
    var currentUser = document.getElementById('user-data').getAttribute('data-current-user');
    var displayStart = 0;
    var displayLimit = 6;

    $(".load_message").click(function() {
        displayNextMessages();
    });

    $(".friend").click(function() {
        var userId = $(this).data("user-id");
        var csrfToken = $('meta[name="csrf-token"]').attr('content');
        var hostPort = $('meta[name="host-port"]').attr('content');

        $.ajax({
            url: hostPort + "get_messages/" + userId + "/",
            type: "POST",
            data: {
                csrfmiddlewaretoken: csrfToken,
            },
            success: function(data) {
                if (Array.isArray(data.messages) && data.messages.length > 0) {
                    $(".load_message").html('<i class="fas fa-sync-alt"></i>');
                    $(".message_block_container").empty();
                    messageHistory = data.messages.reverse(); // Выводим сообщения в обратном порядке
                    displayStart = 0;
                    displayNextMessages();
                } else {
                    $(".load_message").empty();
                    $(".message_block_container").empty();
                    var messageHtml = '<div class="message-not">';
                    messageHtml += '<h2>' + 'Нет сообщений' + '</h2>';
                    messageHtml += '</div>';
                    $(".message_block_container").append(messageHtml);
                }
            },
            error: function() {
                alert("Произошла ошибка при выполнении запроса.");
            },
        });
    });

    function displayNextMessages() {
        for (var i = displayStart; i < Math.min(displayStart + displayLimit, messageHistory.length); i++) {
            var message = messageHistory[i];
            var messageHtml = '<div class="message-item';

            if (currentUser == message.sender) {
                messageHtml += ' sender';
            }

            messageHtml += '">' +
                '<strong>' + message.sender + '</strong>' +
                '<p>' + message.message + '</p>' +
                '<small>' + message.timestamp + '</small>' +
                '</div>';

            $(".message_block_container").prepend(messageHtml); // Добавляем сообщения сверху блока
        }

        displayStart += displayLimit;
    }
});
