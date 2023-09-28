  $(document).ready(function() {
    var csrfToken = $('meta[name="csrf-token"]').attr('content');
    $(".game_add").click(function() {

      // Отправляем Ajax-запрос на сервер для удаления поста
      $.ajax({
        url: "http://127.0.0.1:8888/game_add_profile/", // URL для удаления поста
        type: "POST",
        data: {
          csrfmiddlewaretoken: csrfToken, // CSRF-токен для безопасности
        },
        success: function(data) {
          if (data.result === 'Success') {
            currentPost.hide();
          } else {
            // Обработка ошибки при удалении поста
            alert("Ошибка при загрузке игры!");
          }
        },

        error: function() {
          // Обработка ошибки при Ajax-запросе
          alert("Произошла ошибка при выполнении запроса.");
        },
      });
    });
  });