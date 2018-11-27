import React, { Component } from "react";
import PropTypes from "prop-types";
class DataProvider extends Component {
  static propTypes = {
    endpoint: PropTypes.string.isRequired,
    render: PropTypes.func.isRequired,
    routeId: PropTypes.string,
    sailingId: PropTypes.string
  };
  state = {
      data: [],
      loaded: false,
      placeholder: "Loading..."
    };
  componentDidMount() {
    let endpoint = this.props.endpoint;
    if (this.props.routeId)
      endpoint += "/route/" + this.props.routeId;
    else if (this.props.sailingId)
      endpoint += "/" + this.props.sailingId;

    fetch(endpoint)
      .then(response => {
        if (response.status !== 200) {
          return this.setState({ placeholder: "Something went wrong" });
        }
        return response.json();
      })
      .then(data => this.setState({ data: data, loaded: true }));
  }
  render() {
    const { data, loaded, placeholder } = this.state;
    return loaded ? this.props.render(data) : <p>{placeholder}</p>;
  }
}
export default DataProvider;
