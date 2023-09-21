$(document).ready(function() {
  $(".post_container").hide(); //скрываем котнтейнер с постами
  $("[data-toggle^='post']").click(function() {
    $(".post_container").toggle(); // Переключаем видимость всех контейнеров постов
  });
});