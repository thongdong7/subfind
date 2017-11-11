import React from "react";
import { Button, message } from "antd";
import { connect } from "react-redux";
import { loadReleases } from "../../actions";

const ReloadButton = ({ reload, loading }) => {
  return (
    <Button onClick={reload} loading={loading} icon="reload">
      Reload
    </Button>
  );
};

const mapStateToProps = state => ({
  loading: state.releases.loading,
});
const mapDispatchToProps = dispatch => ({
  reload: async () => {
    await dispatch(loadReleases());
    message.info("Reload complete!");
  },
});
export default connect(mapStateToProps, mapDispatchToProps)(ReloadButton);
