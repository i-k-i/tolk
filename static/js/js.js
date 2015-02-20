var cl = function(message){
    var args = Array.prototype.slice.call(arguments);
    message = args.length === 0 ?
        '----------':args.length === 1 ?
        message: args.join(' ');

    console.log(message);
};

$(document).ready(function() {
  // this initializes the dialog (and uses some common options that I do)
    $(function() {
        var taskDonedialog = $("#done_dialog").dialog({
            autoOpen: false,
            modal: true,
            show: "blind",
            hide: "blind",
            resize: false,
            buttons: {
                "Done task": function () {
                    $('#done_dialog').submit();
                },
                cancel: function () {
                    taskDoneDialog.dialog('close');
                }
            }
        });
    });

    // next add the onclick handler
    $("#task_done").click(function() {
      $("#done_dialog").dialog("open");
    });

//    //only numbers and .
//    $('#digress').keyup(function () {
//      this.value = this.value.replace(/[^0-9\.]/g,'');
//    });
//
});
$(function(){
    $('#search_achievement_kit').keyup(function(){
        $.ajax({
            type: "POST",
            url: "/achievement/search_kit/",
            data:{
                'search_text':$('#search_achievement_kit').val(),
                'csrfmiddlewaretoken': $("input[name=csrfmiddlewaretoken]").val()
            },
            success: searchSuccess,
            dataType: 'html'
        });
    });
});

function searchSuccess(data, textStatus, jqXHR) {
    $('#search_kit_results').html(data);
}
