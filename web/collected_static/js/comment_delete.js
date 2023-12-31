$(document).ready(function() {
    $(document).on("click", ".delete-comment", function() {
        var commentId = $(this).data("comment-id");


        // Установка commentId в модальном окне для последующего удаления
        $("#confirmDelete").data("comment-id", commentId);

        // Отображение модального окна
            $("#confirmDeleteModal").modal("show");
        });


    $("#confirmDelete").click(function() {
        var postId = $(".fa-lg").data("post-id");
        var commentId = $(this).data("comment-id");
        var currentComment = $(".delete-comment[data-comment-id='" + commentId + "']").closest(".comment");
        var commentCountElement = $(`[data-toggle="comments-${postId}"]`);
        var csrfToken = $('meta[name="csrf-token"]').attr('content');
        var hostPort = $('meta[name="host-port"]').attr('content');

      // Отправляем Ajax-запрос на сервер для удаления комента
      $.ajax({
        url: hostPort + "delete_comment/" + commentId + "/", // URL для удаления комента
        type: "POST",
        data: {
          csrfmiddlewaretoken: csrfToken, // CSRF-токен для безопасности
        },
        success: function(data) {
          if (data.success) {
            currentComment.hide();

            var commentCount = parseInt(commentCountElement.data('comment-count'), 10);
            commentCountElement.data('comment-count', commentCount - 1); // Обновляем атрибут data-commen-count
            commentCountElement.text(commentCount - 1); // Обновляем текст элемента


          } else {
            // Обработка ошибки при удалении поста
            alert("Ошибка при удалении комента: " + data.error);
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