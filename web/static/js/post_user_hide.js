$(document).ready(function() {
  $(".post_container").hide(); //скрываем котнтейнер с постами
  $("[data-toggle^='post']").click(function() {
    $(".friends_container").hide();
    $(".post_container").toggle(); // Переключаем видимость всех контейнеров постов
  });
});