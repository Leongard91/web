document.addEventListener('click', event => {
    
    // Edit post code
    if (event.target.id === "edit" && document.querySelector('#back') === null) {

        // Save previous post info
        const previous = event.target.parentElement.innerHTML;
        const previous_id = event.target.parentElement.dataset.post_id;
        const previous_text = document.querySelector(`#post_text_${event.target.value}`).innerHTML;
        class App extends React.Component  {

            // Create state
            constructor(props) {
                super(props);
                this.state = {
                    text: this.props.previous_text
                };
            }

            // Change text varible in state
            newValueiInsert = (event) => {
                this.setState({
                    text: event.target.value
                });
            }

            // insert new text in db
            put = () => {   
                fetch(`/post_reduction/${this.props.previous_id}`, {
                    method: 'PUT',
                    body: JSON.stringify({
                        post_id: this.props.previous_id,
                        new_text: this.state.text
                    })
                });    
            }

            render() {

                // set global varible for new seved post's text
                window.new_textw = this.state.text;

                // create edit form
                return (
                    <div className="">
                        <textarea name="post" cols="40" rows="10" className="edit_area" maxLength="255" id="id_post" onChange={this.newValueiInsert}>
                            {this.props.previous_text}
                        </textarea>
                        <input type="submit" className="btn btn-primary" onClick={this.put} id="save_button" value="Save" />
                        <button type="button" className="btn btn-link" id='back'>Back</button>
                    </div>
                );
            };

        }

        ReactDOM.render(<App previous_text={previous_text} previous_id={previous_id} />, document.querySelector(`#post_${event.target.value}`));
        
        // Return pos with unchanged text if back clicked
        document.querySelector("#back").addEventListener('click', () => {
            document.querySelector(`#post_${event.target.value}`).innerHTML = previous;
        });

        // Return pos with changed text if save clicked
        document.querySelector("#save_button").addEventListener('click', () => {
            document.querySelector(`#post_${event.target.value}`).innerHTML = previous;
            document.querySelector(`#post_text_${event.target.value}`).innerHTML = window.new_textw;
        });
    }


    // Likes
    if (event.target.className === 'hart' && event.target.dataset.is_auth === "True") {
        var action = '';
        if (event.target.dataset.liked === 'false') {
            event.target.src = "static/network/filled_hart.png";
            event.target.dataset.liked = 'true';
            action = 'add';
        } else {
            event.target.src = "static/network/empty_hart.png";
            event.target.dataset.liked = 'false';
            action = 'dell';
        }

        fetch('/like', {
            method: 'PUT',
            body: JSON.stringify({
                post_id: event.target.dataset.post_id,
                movement: action
            })
        }).then(response => response.json())
        .then(data => {
            document.querySelector(`#likes_count_${data.post_id}`).innerHTML = data.likes_count;
        });

        
    }

    return false;
});
