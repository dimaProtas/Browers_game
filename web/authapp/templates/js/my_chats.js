function chatClick(user_id) {
    // Generate the URL using the 'user_id' and the '{% url %}' template tag
    var url = "{% url 'create_chat' user_id=user_id %}";

    // Redirect to the generated URL or perform other actions
    window.location.href = url;
}