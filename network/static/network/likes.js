document.addEventListener('DOMContentLoaded', function() {

    document.addEventListener('click', event => {
        //Get parent of the target of the event
        const element = event.target;

        if (element.id === 'like_button'){

            //Get parent element 
            const post_div = element.parentElement;

            //Get id of the post clicked on
            const post_id = parseInt(post_div.dataset.post_id);
            console.log(post_id);

            //Check whether the post is liked
            like_icon = post_div.querySelector('#like_button');

            if(like_icon.className == 'bi bi-suit-heart-fill'){

                //The post is already liked, so we dislike it
                fetch(`/post/${post_id}`, {
                    method: 'PUT',
                    body: JSON.stringify({
                        like: false
                    })
                  })
                .then(response => response.json())
                .then(result => {
                    console.log(result);
                });
                //Change the icon to a non-liked configuration
                like_icon.className = 'bi bi-suit-heart';

                //decrase likes counter
                let likes_number = parseInt(post_div.querySelector('#likes_number').innerHTML);
                post_div.querySelector('#likes_number').innerHTML = `${likes_number-1}`;

            }else{
                //The post is not-liked, so we like it
                fetch(`/post/${post_id}`, {
                    method: 'PUT',
                    body: JSON.stringify({
                        like: true
                    })
                  })
                .then(response => response.json())
                .then(result => {
                    console.log(result);
                });
                //Change the icon to a non-liked configuration
                like_icon.className = 'bi bi-suit-heart-fill';

                //decrase likes counter
                let likes_number = parseInt(post_div.querySelector('#likes_number').innerHTML);
                post_div.querySelector('#likes_number').innerHTML = `${likes_number+1}`;
            }

        }
        
    });
   
    
  });