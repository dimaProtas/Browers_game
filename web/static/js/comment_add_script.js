$(document).ready(function() {
    var csrfToken = $('meta[name="csrf-token"]').attr('content');
    var hostPort = $('meta[name="host-port"]').attr('content');

    // Обработчик события для поля ввода комментария
    $(".comment-input").keypress(function(event) {
        if (event.which === 13) { // Проверяем, была ли нажата клавиша Enter (код 13)
            event.preventDefault(); // Предотвращаем стандартное действие Enter (обычно отправка формы)

            // Находим ближайшую форму с атрибутом data-comment-form
            var commentFormId = $(this).closest('form').data("comment-form");

            // Находим иконку отправки сообщения внутри формы с этим ID
            var submitIcon = $(`[data-comment-form="${commentFormId}"] .fa-lg`);

            // Вызываем функцию отправки сообщения для этой иконки
            submitIcon.click();
        }
    });


    $(".fa-lg").click(function() {
        var postId = $(this).data("post-id");
        var commentFormId = $(this).data("comment-form");
        var commentInput = $(`[data-comment-form="${commentFormId}"] input[name="content"]`);
        var comment = commentInput.val();
        var commentCountElement = $(`[data-toggle="comments-${postId}"]`);

        if (comment !== '') {
            // var postData = {
            //     csrfmiddlewaretoken: csrfToken,
            //     comment: comment
            // };
            // Отправляем Ajax-запрос на сервер для сохранения комента
            $.ajax({
            url: hostPort + "add_comment/" + postId + "/",
            type: "POST",
            data: {
                csrfmiddlewaretoken: csrfToken,
                comment: comment
            },
            // data: JSON.stringify(postData), // Преобразование в JSON
            // contentType: "application/json",
            success: function(data) {
                if (data.result === 'Success') {

                   var commentContainer = $("#comments-" + postId); // Находим контейнер комментариев

                   // Создаем новый HTML-элемент для комментария
                    var newComment = '<div class="comment">' +
                        '<div class="comment_date">' +
                            '<span class="author">' + data.author + '</span>' +
                            '<div>' +
                            '<span class="date_time">' + data.created_at + '</span>' +
                            '<i class="fas fa-times delete-comment" data-comment-id=' + data.comment_id + '>' + '</i>' +
                            '</div>' +
                        '</div>' +
                            '<div class="content">' + data.content + '</div>' +
                        '</div>';
                        '</div>';

                    // Проверяем, видим ли контейнер
                    if (commentContainer.is(":visible")) {
                        // Если контейнер видим, оставляем его открытым и просто добавляем новый комментарий
                        commentContainer.prepend(newComment);
                    } else {
                        // Если контейнер скрыт, открываем его и добавляем новый комментарий
                        commentContainer.show().prepend(newComment);
                    }

                    var commentCount = parseInt(commentCountElement.data('comment-count'), 10);
                    commentCountElement.data('comment-count', commentCount + 1); // Обновляем атрибут data-commen-count
                    commentCountElement.text(commentCount + 1); // Обновляем текст элемента

                    // Очищаем поле ввода комментария
                    commentInput.val('');
                } else if (data.message === 'Empty comment') {
                    alert("Нельзя отправлять пустой коментарий!");
                }
            },
            error: function(xhr, status, error) {
                // Обработка ошибки при Ajax-запросе
                console.log("Ajax request failed:", status, error);
                alert("Произошла ошибка при выполнении запроса.");
            },
        });
        } else {
            alert('Нельзя отправлять пустой коментарий!')
        }

    });
});