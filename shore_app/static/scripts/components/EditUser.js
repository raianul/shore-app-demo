import React from 'react';
import UserForm from './UserForm';
import fetchAPI from './Api';

class EditUser extends React.Component {
  // Adapted from - https://reactjs.org/docs/faq-ajax.html

  constructor(props) {
    super(props);
    this.state = {
      error: null,
      isLoaded: false,
      item: null
    };
  }
  async componentDidMount() {
    const id = this.props.match.params.id;
    try {
      const response = await fetchAPI("GET", '/api/user/' + id);
      if (response.ok) {
        let data = await response.json();
        this.setState({
          isLoaded: true,
          item: data
        });
      } else {
        return response;
      }
    } catch (error) {
      this.setState({
        isLoaded: true,
        error
      });
    }
  }


  render() {
    const { error, isLoaded, item } = this.state;
    let errorDiv = '';
    if (error) {
      errorDiv = 'Error: ' + error.message;
    } else if (!isLoaded) {
      return <div>Loading...</div>;
    }
    return (
      <div>
        {errorDiv}
        <UserForm user={item} handleOnSubmit={this.handleOnSubmit.bind(this)} />
      </div>
    );
  }

  async handleOnSubmit(user) {
    const id = this.state.item.id;
    const response = await fetchAPI("PUT", '/api/user/' + id, user);
    if (response.ok) {
      this.props.history.push("/");
    } else {
      const resp = await response.json()
      const error = {
        message: resp.message
      }
      this.setState({
        isLoaded: false,
        error: error
      });
      // this.props.history.push("/user/edit" + id);
    }
  }
}



export default EditUser;
