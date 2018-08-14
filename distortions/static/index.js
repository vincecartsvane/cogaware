function delete_trap(trap_id) {
    var form = $('form[name="delete"]');
    form.submit(function(ev) {
	ev.preventDefault();
    });
    var token = $('form[name="delete"] > input[name="csrfmiddlewaretoken"]').val();

    $.ajax({
	url: "" + trap_id,
	type: "DELETE",
	beforeSend: function(xhr) {
            xhr.setRequestHeader("X-CSRFToken", token);
	},
	success: function() {
	    location.reload()
	},
    });
}
