    function add_to_watchlist(id){
        movie_row = $('tr#moviedb_id_'+id);
        movie_row.find('td > div.text').text("watching");
        return false;
    }

    function bind_add_movie_to_watchlist_buttons(){
        button = $('button.movie[data_moviedb_id='+movie_id+']');
        button.click({movie_id:movie_id}, function(event){
            movie_id = event.data.movie_id;
            button = $('button.movie[data_moviedb_id='+movie_id+']');
            console.log('ajaxing adding-to-watchlist '+movie_id);
            button.removeClass('btn-primary');
            button.addClass('btn-success');
            button.find('span.text').text("Watching");
            $.ajax({
                url: '/watchlist/1/add/'+movie_id+'/',
            })
        });
    }
