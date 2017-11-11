import React from "react";
import { Table, Layout, message } from "antd";
import { connect } from "react-redux";
import LanguageStats from "./LanguageStats";
import SFReleaseFilter from "./Filter";
import RPCLink from "../RPCLink";
import RPCButton from "../RPCButton";
import { updateShowMissed, loadReleases } from "../../actions";
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
    const { columns, dataSource } = this.props;

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
        </Header>

        <Content style={{ padding: "0 50px", backgroundColor: "white" }}>
          <SFReleaseFilter />

          <Table columns={columns} dataSource={dataSource} size="small" />
        </Content>
      </Layout>
    );
  }

  onScanAllComplete = () => {
    this.props.loadData();

    message.info("Scan all complete!");
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
  const { items } = state.releases;
  const dataSource = doFilter(items, state.filter).map((item, i) => ({
    ...item,
    key: i,
  }));

  return {
    dataSource,
    // releases: state.releases,
    filter: state.filter,
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
