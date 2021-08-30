import React from 'react';
import SubscriptionForm from './SubscriptionForm';
import fetchAPI from './Api';

class EditSubscription extends React.Component {
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
      const response = await fetchAPI("GET", '/api/subscription/' + id);
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
        <SubscriptionForm subscription={item} handleOnSubmit={this.handleOnSubmit.bind(this)} />
      </div>
    );
  }

  async handleOnSubmit(subscription) {
    const id = this.state.item.id;

    const response = await fetchAPI("PUT", '/api/subscription/' + id, subscription);
    if (response.ok) {
      this.props.history.push("/user/" + subscription.user_id + "/subscriptions");
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
  }
}



export default EditSubscription;
