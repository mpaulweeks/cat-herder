
function setUpListeners(){
    // ajax goes here
    $('.vote').click(function (){
        var $this = $(this);
        $this.toggleClass("True");
    });
}
