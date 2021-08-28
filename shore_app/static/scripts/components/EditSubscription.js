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
    if (error) {
      return <div>Error: {error.message}</div>;
    } else if (!isLoaded) {
      return <div>Loading...</div>;
    } else {
      return (
        <div>
          <SubscriptionForm subscription={item} handleOnSubmit={this.handleOnSubmit.bind(this)} />
        </div>
      );
    }
  }

  async handleOnSubmit(subscription) {
    console.log(subscription);
    const id = this.state.item.id;
    const response = await fetchAPI("PUT", '/api/subscription/' + id, subscription);
    if (response.ok) {
      this.props.history.push("/user/" + subscription.user_id + "/subscriptions");
    } else {
      const error = {
        message: response.statusText
      }
      this.setState({
        isLoaded: false,
        error: error
      });
    }
  }
}



export default EditSubscription;
