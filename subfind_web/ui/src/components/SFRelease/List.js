// @flow
import { Button, Layout, Progress, Table } from "antd";
import React from "react";
import { connect } from "react-redux";
import { Link } from "react-router-dom";
import { updateShowMissed, loadReleases } from "../../actions";
import RPCButton from "../RPCButton";
import RPCLink from "../RPCLink";
import SFReleaseFilter from "./Filter";
import LanguageStats from "./LanguageStats";
import ReloadButton from "./ReloadButton";
const { Header, Content } = Layout;

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
      columns,
      dataSource,
      scanningRelease: { releaseName, index, total },
    } = this.props;

    return (
      <Layout>
        <Header>
          <ReloadButton />
          <RPCButton
            name="Scan All"
            icon="scan"
            query="/api/Release/scan_all"
            onComplete={this.onScanAllComplete}
          />
          <Link to="/config">
            <Button>Config</Button>
          </Link>
        </Header>

        {releaseName && (
          <span>
            <Progress
              status="active"
              strokeWidth={5}
              percent={Math.floor((index + 1) * 100 / total)}
            />
            Downloading release [<strong>{index + 1}</strong> /{" "}
            <strong>{total}</strong>] {releaseName} ...
          </span>
        )}
        <Content style={{ padding: "0 50px", backgroundColor: "white" }}>
          <SFReleaseFilter />

          <Table columns={columns} dataSource={dataSource} size="small" />
        </Content>
      </Layout>
    );
  }

  onScanAllComplete = () => {
    this.props.loadData();
  };
}

function doFilter(releases, { showMissed, onlyShowLang }) {
  return releases
    .filter(i => !showMissed || Object.keys(i.subtitles).length === 0)
    .filter(
      i =>
        Object.keys(i.subtitles).filter(l => onlyShowLang.indexOf(l) >= 0)
          .length === 0
    );
}

const mapStateToProps = state => {
  const { items, scanningRelease } = state.releases;
  const dataSource = doFilter(items, state.filter).map((item, i) => ({
    ...item,
    key: i,
  }));

  return {
    dataSource,
    // releases: state.releases,
    filter: state.filter,
    scanningRelease,
  };
};

const mapDispatchToProps = (dispatch: Function) => {
  return {
    loadData: () => dispatch(loadReleases()),
    setShowMissed: value => dispatch(updateShowMissed(value)),
    columns: [
      {
        title: "Release",
        dataIndex: "release_name",
        key: "release_name",
        render: (text, record) => (
          <span>
            {record.release_name}
            <LanguageStats data={record.subtitles} />
          </span>
        ),
      },
      {
        title: "Action",
        key: "action",
        render: (text, record) => (
          <span>
            <RPCLink
              name="Download"
              icon="cloud-download"
              query="/api/Release/download"
              params={{ src: record.src, name: record.name }}
              onComplete={() => dispatch(loadReleases())}
            />
            <span className="ant-divider" />
            <RPCLink
              name="Remove subtitles"
              icon="delete"
              query="/api/Release/remove_subtitle"
              params={{ src: record.src, name: record.name }}
              onComplete={() => dispatch(loadReleases())}
            />
            <span className="ant-divider" />
            <a
              href={`https://subscene.com/subtitles/title?q=${record.title_query}&l=`}
              target="subscence"
            >
              <i className="fa fa-bug" /> Subscene
            </a>
          </span>
        ),
      },
    ],
  };
};

export default connect(mapStateToProps, mapDispatchToProps)(SFReleaseList);
