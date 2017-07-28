import React from "react";
import _ from "lodash";
import * as tb from "tb-react";
// import Button from "antd/lib/button";
import { Table, Icon, Button } from "antd";
import { connect } from "react-redux";
import LanguageStats from "./LanguageStats";
import SFReleaseFilter from "./Filter";
import RPCLink from "../RPCLink";
import { updateShowMissed, loadReleases } from "../../actions";

class SFReleaseList extends React.Component {
  constructor(props, context) {
    super(props, context);

    this.state = {
      showMissed: true,
      onlyShowLang: [],
    };
    this.props.loadData();
  }

  render() {
    const {
      reload,
      onScanComplete,
      onRemoveComplete,
      columns,
      dataSource,
    } = this.props;
    return (
      <div className="box box-solid">
        <div className="box-header with-border">
          <h3 className="box-title">Movies</h3>

          <div className="box-tools">
            <Button type="primary">Reload</Button>
            <Button type="primary">Scan All</Button>
            <Button type="primary">Setup</Button>
            {/* <tb.APIActionButton
              name="Reload"
              icon="refresh"
              type="info"
              action={[releaseActions.load]}
            />

            <tb.RemoteButton
              url="Release/scan-all"
              name="Scan All"
              icon="tasks"
              onComplete={onScanComplete}
            />

            <tb.LinkButton to="/release/config" icon="cog" name="Setup" /> */}
          </div>
        </div>
        <div className="box-body">
          <SFReleaseFilter />

          <Table columns={columns} dataSource={dataSource} />

          {/* {this.releases.map((item, k) => {
            let stateClass = "";
            if (_.isEmpty(item.subtitles)) {
              stateClass = " bg-warning";
            }
            return (
              <div
                key={k}
                className={"row row-hover row-list-item" + stateClass}
              >
                <div className="col-lg-10 col-xs-12">
                  {item.name}
                </div>
                <div className="col-lg-1 col-xs-10">
                  <LanguageStats data={item.subtitles} />
                </div>
                <div className="col-lg-1 col-xs-2">
                  <tb.RemoteButton
                    url="Release/download"
                    params={{ src: item.src, name: item.name }}
                    icon="download"
                    onComplete={reload}
                    name="Download"
                    type="info"
                  />
                  <tb.RemoteButton
                    url="Release/remove-subtitle"
                    params={{ src: item.src, name: item.name }}
                    icon="trash"
                    onComplete={onRemoveComplete}
                    name="Remove Subtitles"
                    type="danger"
                  />
                  <a
                    href={`https://subscene.com/subtitles/title?q=${item.title_query}&l=`}
                    target="subscence"
                  >
                    <i className="fa fa-bug" /> Subscene
                  </a>
                </div>
              </div>
            );
          })} */}
        </div>
      </div>
    );
  }
}

SFReleaseList.contextTypes = {
  router: React.PropTypes.object,
};

function doFilter(releases, { showMissed, onlyShowLang }) {
  console.log("showMissed", showMissed);
  return releases
    .filter(i => !showMissed || Object.keys(i.subtitles).length === 0)
    .filter(
      i =>
        Object.keys(i.subtitles).filter(l => onlyShowLang.indexOf(l) >= 0)
          .length === 0
    );
}

const mapStateToProps = state => {
  const dataSource = doFilter(state.releases, state.filter).map((item, i) => ({
    ...item,
    key: i,
  }));
  const columns = [
    {
      title: "Release",
      dataIndex: "release_name",
      key: "release_name",
      render: (text, record) =>
        <span>
          {record.release_name}
          <LanguageStats data={record.subtitles} />
        </span>,
    },
    {
      title: "Action",
      key: "action",
      render: (text, record) =>
        <span>
          <RPCLink
            name="Download"
            icon="cloud-download"
            query="/api/Release/download"
            params={{ src: record.src, name: record.name }}
          />
          <span className="ant-divider" />
          <a href="#">
            <Icon type="delete" /> Delete
          </a>
          <span className="ant-divider" />
          <a
            href={`https://subscene.com/subtitles/title?q=${record.title_query}&l=`}
            target="subscence"
          >
            <i className="fa fa-bug" /> Subscene
          </a>
        </span>,
    },
  ];

  return {
    dataSource,
    columns,
    releases: state.releases,
    filter: state.filter,
  };
};

const mapDispatchToProps = (dispatch: Function) => {
  return {
    loadData: () => dispatch(loadReleases()),
    setShowMissed: value => dispatch(updateShowMissed(value)),
  };
};

export default connect(mapStateToProps, mapDispatchToProps)(SFReleaseList);
