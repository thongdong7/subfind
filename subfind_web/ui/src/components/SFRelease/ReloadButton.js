import React from "react";
import { Button } from "antd";
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
  reload: () => dispatch(loadReleases()),
});
export default connect(mapStateToProps, mapDispatchToProps)(ReloadButton);
