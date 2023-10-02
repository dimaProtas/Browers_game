  $(document).ready(function() {
    var csrfToken = $('meta[name="csrf-token"]').attr('content');
    var hostPort = $('meta[name="host-port"]').attr('content');
    $(".game_add").click(function() {

      // Отправляем Ajax-запрос на сервер для удаления поста
      if (userIsAuthenticated) {
      $.ajax({
        url: hostPort + "game_add_profile/", // URL для удаления поста
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
      }
    });
  });