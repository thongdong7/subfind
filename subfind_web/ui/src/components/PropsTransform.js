// @flow
import React, { Component } from "react";
import isEqual from "lodash/isEqual";

type TTransformFunc = Object => Object;

/**
 * HOC: Transform props to another props
 * 
 * @param {Function[]} transforms Transform functions
 */

const SUCCESS = "SUCCESS";
const FAILURE = "FAILURE";
const NOT_ASKED = "NOT_ASKED";
const PENDING = "PENDING";

type TNotAsked = {
  type: "NOT_ASKED",
};

type TPending = {
  type: "PENDING",
};

type TFailure = {
  type: "FAILURE",
  error: string,
};

type TSuccess = {
  type: "SUCCESS",
  data: {
    [field: string]: any,
  },
};

type TState = TNotAsked | TPending | TFailure | TSuccess;

const defaultOptions = {
  isPropsChanged: (props, nextProps) => true,
};

export default (transformFunc: TTransformFunc, options = defaultOptions) => (
  Comp: Class<React$Component<void, {}, void>>
) => {
  const { isPropsChanged } = options;
  return class extends Component<void, Object, TState> {
    state = {
      type: NOT_ASKED,
    };

    componentWillMount() {
      this.loadProps(this.props);
    }

    componentWillReceiveProps(nextProps: Object) {
      // Only transform props if props is changed
      if (isPropsChanged(this.props, nextProps)) {
        this.loadProps(nextProps);
      }
    }

    loadProps = async (props: Object) => {
      // $FlowFixMe
      this.setState({ type: PENDING });
      try {
        const nextProps = await transformFunc(props);
        // $FlowFixMe
        this.setState({
          type: SUCCESS,
          data: nextProps,
        });
      } catch (e) {
        /* eslint-disable no-console */
        console.error(e);
        /* eslint-enable no-console */
        // $FlowFixMe
        this.setState({
          type: FAILURE,
          error: e.message,
        });
      }
    };

    render() {
      const { type } = this.state;

      switch (type) {
        case NOT_ASKED:
          return null;
        case PENDING:
          return <div>Loading...</div>;
        case FAILURE:
          // $FlowFixMe
          return (
            <div>
              Error:
              {this.state.error}
            </div>
          );
        case SUCCESS:
          // $FlowFixMe
          return <Comp {...this.state.data} />;

        default:
          return null;
      }
    }
  };
};
