$(document).ready(() => {
    let genreSelection = [];
    let genreSelectionId = null;

    $(document).on('click', '.genre', function(){
        let elem = $(this);
        $('.genre').each(function() { 
            if($(this).data() != elem.data())
                $(this).removeClass('badge-info');
        });

        if (elem.hasClass('badge-info')) {
            genreSelectionId = null;
            elem.removeClass('badge-info');
        } else {
            genreSelectionId = elem.data('genre');
            elem.addClass('badge-info');
        };
    });

    $('#genre-filter').click(function(e) {
        e.preventDefault();
        $('.game-container').each(function() { 
            if($(this).data("genre") == genreSelectionId || genreSelectionId == null)
                $(this).css('display', 'inline');
            else
                $(this).css('display', 'none');
        });
    });
});