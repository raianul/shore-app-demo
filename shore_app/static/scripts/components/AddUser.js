import React from 'react';
import UserForm from './UserForm';
import fetchAPI from './Api';

class AddUser extends React.Component {
  // Adapted from - https://reactjs.org/docs/faq-ajax.html

  constructor(props) {
    super(props);
    this.state = {
      error: null,
    };
  }

  render() {
    const { error } = this.state;
    let errorDiv = '';
    if (error) {
      errorDiv = 'Error: ' + error.message;
    }
    return (
      <div>
        {errorDiv}
        <UserForm handleOnSubmit={this.handleOnSubmit.bind(this)} />
      </div>
    );

  }

  async handleOnSubmit(user) {
    try {
      const response = await fetchAPI("POST", '/api/users', user);
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
      }
    } catch (error) {
      this.setState({
        isLoaded: false,
        error: error.message
      });
    }
  }
}



export default AddUser;
