import React from 'react';
import SubscriptionForm from './SubscriptionForm';
import fetchAPI from './Api';

class AddSubscription extends React.Component {
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
        <SubscriptionForm handleOnSubmit={this.handleOnSubmit.bind(this)} />
      </div>
    );
  }

  async handleOnSubmit(subscription) {
    try {
      const response = await fetchAPI("POST", '/api/subscriptions', subscription);
      if (response.ok) {
        const responJson = await response.json();
        this.props.history.push('/user/' + responJson.user_id + '/subscriptions');
      } else {
        const resp = await response.json();
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



export default AddSubscription;
