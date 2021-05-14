document.addEventListener('click', event => {
    if (event.target.id === "edit") {
        const previous = event.target.parentElement.innerHTML;
        const previous_text = document.querySelector(`#post_text_${event.target.value}`).innerHTML;
        
        class App extends React.Component  {

            render() {
                return (
                    <div className="form_area">
                        <br/>
                        <textarea name="post" cols="40" rows="10" className="post_form" maxLength="255" id="id_post">
                            {this.props.previous_text}
                        </textarea>
                        <input type="submit" className="btn btn-primary" id="post_button" value="Save" />
                        <button type="button" className="btn btn-link" onClick={this.back} id='back'>Back</button>
                    </div>
                );
            };

        }

        ReactDOM.render(<App previous_text={previous_text} />, document.querySelector(`#post_${event.target.value}`));
        
        document.querySelector("#back").addEventListener('click', () => {
            document.querySelector(`#post_${event.target.value}`).innerHTML = previous;
        });
    }
    return false;
});