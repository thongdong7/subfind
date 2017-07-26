import React from "react";
import _ from "lodash";
import * as tb from "tb-react";
// import Button from "antd/lib/button";
import { Table, Icon, Button } from "antd";

import LanguageStats from "./LanguageStats";
import SFReleaseFilter from "./Filter";
import { releaseActions } from "../../actions/release";
import PropsTransform from "../PropsTransform";
let onBottom;

window.onscroll = function(ev) {
  if (window.innerHeight + window.scrollY + 100 >= document.body.offsetHeight) {
    if (onBottom) {
      onBottom();
    }
    // console.log('bottom', onBottom);
  }
};

class SFReleaseList extends React.Component {
  constructor(props, context) {
    super(props, context);

    this.state = {
      page: 1,
    };

    this.limit = 20;
    this.maxPage = props.releases.length / this.limit;
  }

  componentWillReceiveProps(nextProps) {
    this.maxPage = nextProps.releases.length / this.limit;
  }

  componentWillMount() {
    onBottom = this.onBottom;
  }

  onBottom = () => {
    // console.log('page', this.state.page, this.maxPage, this.props.releases.length);
    if (this.state.page >= this.maxPage) {
      return;
    }

    let nextPage = this.state.page + 1;
    this.setState({
      page: nextPage,
    });
    // console.log('b', nextPage);
  };

  get releases() {
    return this.props.releases.slice(0, this.state.page * this.limit);
  }

  render() {
    // console.log('render', this.state.filteredData.length);
    // console.log('props', this.props);
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

          {this.releases.map((item, k) => {
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
                  <Button icon="cloud-download">Download</Button>
                  <Button type="danger" icon="delete">
                    Remove Subtitle
                  </Button>
                  {/* <tb.RemoteButton
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
                  /> */}
                  <a
                    href={`https://subscene.com/subtitles/title?q=${item.title_query}&l=`}
                    target="subscence"
                  >
                    <i className="fa fa-bug" /> Subscene
                  </a>
                </div>
              </div>
            );
          })}
        </div>
      </div>
    );
  }
}

SFReleaseList.contextTypes = {
  router: React.PropTypes.object,
};

function doFilter(releases, { onlyShowMissedSubtitle, onlyShowLang }) {
  return releases
    .filter(
      i => !onlyShowMissedSubtitle || Object.keys(i.subtitles).length === 0
    )
    .filter(
      i =>
        Object.keys(i.subtitles).filter(l => onlyShowLang.indexOf(l) >= 0)
          .length === 0
    );
}

// export default tb.connect2({
//   start: dispatch => dispatch(releaseActions.load),
//   props: ({ releases, releaseFilter }, ownProps, dispatch) => ({
//     releases: doFilter(releases, releaseFilter),
//     reload: () => dispatch(releaseActions.load),
//     onRemoveComplete: (res, { name }) => {
//       dispatch(releaseActions.load);
//       tb.success(`Removed subtitles of ${name}`);
//     },
//     onScanComplete: () => {
//       dispatch(releaseActions.load);
//       tb.success("Scan completed");
//     },
//   }),
// })(SFReleaseList);
export default PropsTransform(async props => {
  const res = await fetch(`/api/Release/list`);
  const data = await res.json();

  const dataSource = data.map(item => ({
    ...item,
    key: item.release_name,
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
          <a href="#">
            <Icon type="cloud-download" /> Download
          </a>
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
  console.log(data[0]);
  return {
    releases: data,
    dataSource,
    columns,
  };
})(SFReleaseList);
