//обработчик удаления и добавления лайков
$(document).ready(function() {
    var csrfToken = $('meta[name="csrf-token"]').attr('content');
    var hostPort = $('meta[name="host-port"]').attr('content');

    $(".fa-fire").click(function() {
        var postId = $(this).data("post-id");
        var likeCountElement = $(this);
        console.log(csrfToken)

        if (userIsAuthenticated) {
        // Отправляем Ajax-запрос на сервер для создания или удаления лайков
        $.ajax({
            url: hostPort + "toggle_like/" + postId + "/", // URL для dislike
            type: "POST",
            data: {
                csrfmiddlewaretoken: csrfToken, // CSRF-токен для безопасности
            },
            success: function(data) {
                if (data.message === 'like_add') {
                    // Присваиваем красный цвет текущему элементу
                    likeCountElement.addClass("red-text").removeClass("orange-text");
                    var currentLikeCount = parseInt(likeCountElement.data('like-count'), 10);
                    likeCountElement.data('like-count', currentLikeCount + 1); // Обновляем атрибут data-like-count
                    likeCountElement.text(currentLikeCount + 1); // Обновляем текст элемента
                } else if (data.message === 'like_delete') {
                    // Присваиваем оранжевый цвет текущему элементу
                    likeCountElement.addClass("orange-text").removeClass("red-text");
                    var currentLikeCount = parseInt(likeCountElement.data('like-count'), 10);
                    likeCountElement.data('like-count', currentLikeCount - 1); // Обновляем атрибут data-like-count
                    likeCountElement.text(currentLikeCount - 1); // Обновляем текст элемента
                }
            },
            error: function() {
                // Обработка ошибки при Ajax-запросе
                alert("Произошла ошибка при выполнении запроса.");
            },
        });
        } else {
            // Отображение модального окна
            $("#confirmModal").modal("show");
        }

    });
});


//обработчик удаления и добавления дизлаков
$(document).ready(function() {
    var csrfToken = $('meta[name="csrf-token"]').attr('content');

    $(".fa-thumbs-down").click(function() {
        var postId = $(this).data("post-id");
        var DislikeCountElement = $(this);

        if (userIsAuthenticated) {
            // Отправляем Ajax-запрос на сервер для создания или удаления dislike
            $.ajax({
            url: "http://127.0.0.1:8888/toggle_dislike/" + postId + "/", // URL для dislike
            type: "POST",
            data: {
                csrfmiddlewaretoken: csrfToken, // CSRF-токен для безопасности
            },
            success: function(data) {
                if (data.message === 'dislike_add') {
                    // Присваиваем тёмно-красный цвет текущему элементу
                    DislikeCountElement.addClass("darck-red-text").removeClass("blue-text");
                    var currentDisLikeCount = parseInt(DislikeCountElement.data('dislike-count'), 10);
                    DislikeCountElement.data('dislike-count', currentDisLikeCount + 1); // Обновляем атрибут data-dislike-count
                    DislikeCountElement.text(currentDisLikeCount + 1); // Обновляем текст элемента
                } else if (data.message === 'dislike_delete') {
                    // Присваиваем синий цвет текущему элементу
                    DislikeCountElement.addClass("blue-text").removeClass("darck-red-text");
                    var currentDisLikeCount = parseInt(DislikeCountElement.data('dislike-count'), 10);
                    DislikeCountElement.data('dislike-count', currentDisLikeCount - 1); // Обновляем атрибут data-dislike-count
                    DislikeCountElement.text(currentDisLikeCount - 1); // Обновляем текст элемента
                }
            },
            error: function() {
                // Обработка ошибки при Ajax-запросе
                alert("Произошла ошибка при выполнении запроса.");
            },
        });
        } else {
            $("#confirmModal").modal("show");
        }

    });
});