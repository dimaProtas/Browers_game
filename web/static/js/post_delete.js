  $(document).ready(function() {
    $(".delete-post").click(function() {
        var postId = $(this).data("post-id");

        // Установка postId в модальном окне для последующего удаления
        $("#confirmDelete").data("post-id", postId);

        // Отображение модального окна
            $("#confirmDeleteModal").modal("show");
        });

        $("#confirmDelete").click(function() {
            var postId = $(this).data("post-id");
            var currentPost = $(".delete-post[data-post-id='" + postId + "']").closest(".post");
            var csrfToken = $('meta[name="csrf-token"]').attr('content');
            var hostPort = $('meta[name="host-port"]').attr('content');



      // Отправляем Ajax-запрос на сервер для удаления поста
      $.ajax({
        url: hostPort + "delete_post/" + postId + "/", // URL для удаления поста
        type: "POST",
        data: {
          csrfmiddlewaretoken: csrfToken, // CSRF-токен для безопасности
        },
        success: function(data) {
          if (data.sucses) {
            currentPost.hide();
          } else {
            // Обработка ошибки при удалении поста
            alert("Ошибка при удалении поста: " + data.error);
          }
        },

        error: function() {
          // Обработка ошибки при Ajax-запросе
          alert("Произошла ошибка при выполнении запроса.");
        },
      });
      // Закрытие модального окна после удаления
        $("#confirmDeleteModal").modal("hide");
    });
  });