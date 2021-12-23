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

    //Getting posts
    fetch(`/posts/${posts_set}`)
    .then(response => response.json())
    .then(posts => {
        // Print posts in cosole
        console.log(posts);

        //display each post
        posts.forEach(post => display_post(post));
});
}

////////////////

function display_post(post){

    //Creating div for each post
    let div_post = document.createElement('div');
    div_post.className = "card";

    let body = document.createElement('div');
    body.className = "card-body";
    body.innerHTML = `<h5 class="card-title"> ${post.poster} </h5>`

    let content = document.createElement('p');
    content.className = "card-text";
    content.innerHTML = post.content;

    let timestamp = document.createElement('p');
    timestamp.className = "card-text";
    timestamp.innerHTML = `<small class="text-muted">${post.timestamp}</small>`

    //Assemble post
    body.append(content, timestamp);
    div_post.append(body);
    document.querySelector('#session_posts').append(div_post);


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



