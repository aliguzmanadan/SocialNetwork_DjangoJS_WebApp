document.addEventListener('DOMContentLoaded', function() {

    // Use links in the top of the page to toggle between views
    document.querySelector('#all_posts_link').addEventListener('click', () => load_posts('all'));
    document.querySelector('#following_link').addEventListener('click', () => load_posts('following'));
    document.querySelector('#post_form').addEventListener('submit', () => submit_post());
   
    // By default, load all posts
    load_posts('all');
  });


////////////////

function load_posts(posts_set){
    document.querySelector('#session_name').innerHTML = `<h3>${posts_set.charAt(0).toUpperCase() + posts_set.slice(1)}</h3>`;

}

//////////////////

function submit_post(){
    
    //Get content of the form
    const content = document.querySelector('#content').value; 
    console.log(content)

    //submit the post via POST request to the API
    fetch('/posts', {
        method: 'POST',
        body: JSON.stringify({
            content: content
        })
      })
      .then(response => response.json())
      .then(result => {
          // Print result
          console.log(result);
      });
}



