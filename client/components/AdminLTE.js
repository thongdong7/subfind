import React from 'react'
import { Link } from 'react-router'

export default class AdminLTE extends React.Component {
  constructor(props) {
    super(props)
  }

  render() {
    return (
      <div className="wrapper">

        { /* Main Header */ }
        <header className="main-header">

          { /* Logo */ }
          <a href="/" className="logo">
            { /* mini logo for sidebar mini 50x50 pixels */ }
            <span className="logo-mini"><b>A</b>LT</span>
            { /* logo for regular state and mobile devices */ }
            <span className="logo-lg"><b>Admin</b>LTE</span>
          </a>

          { /* Header Navbar */ }
          <nav className="navbar navbar-static-top" role="navigation">
            { /* Sidebar toggle button*/ }
            <a href="#" className="sidebar-toggle" data-toggle="offcanvas" role="button">
              <span className="sr-only">Toggle navigation</span>
            </a>
            { /* Navbar Right Menu */ }
            <div className="navbar-custom-menu">
              <ul className="nav navbar-nav">
                { /* Messages: style can be found in dropdown.less*/ }
                <li className="dropdown messages-menu">
                  { /* Menu toggle button */ }
                  <a href="#" className="dropdown-toggle" data-toggle="dropdown">
                    <i className="fa fa-envelope-o"></i>
                    <span className="label label-success">4</span>
                  </a>
                  <ul className="dropdown-menu">
                    <li className="header">You have 4 messages</li>
                    <li>
                      { /* inner menu: contains the messages */ }
                      <ul className="menu">
                        <li>{ /* start message */ }
                          <a href="#">
                            <div className="pull-left">
                              { /* User Image */ }
                              <img src="node_modules/admin-lte/dist/img/user2-160x160.jpg" className="img-circle" alt="User Image" />
                            </div>
                            { /* Message title and timestamp */ }
                            <h4>
                              Support Team
                              <small><i className="fa fa-clock-o"></i> 5 mins</small>
                            </h4>
                            { /* The message */ }
                            <p>Why not buy a new awesome theme?</p>
                          </a>
                        </li>
                        { /* end message */ }
                      </ul>
                      { /* /.menu */ }
                    </li>
                    <li className="footer"><a href="#">See All Messages</a></li>
                  </ul>
                </li>

                <li className="dropdown notifications-menu">
                  { /* Menu toggle button */ }
                  <a href="#" className="dropdown-toggle" data-toggle="dropdown">
                    <i className="fa fa-bell-o"></i>
                    <span className="label label-warning">10</span>
                  </a>
                  <ul className="dropdown-menu">
                    <li className="header">You have 10 notifications</li>
                    <li>
                      { /* Inner Menu: contains the notifications */ }
                      <ul className="menu">
                        <li>{ /* start notification */ }
                          <a href="#">
                            <i className="fa fa-users text-aqua"></i> 5 new members joined today
                          </a>
                        </li>
                        { /* end notification */ }
                      </ul>
                    </li>
                    <li className="footer"><a href="#">View all</a></li>
                  </ul>
                </li>
                { /* Tasks Menu */ }
                <li className="dropdown tasks-menu">
                  { /* Menu Toggle Button */ }
                  <a href="#" className="dropdown-toggle" data-toggle="dropdown">
                    <i className="fa fa-flag-o"></i>
                    <span className="label label-danger">9</span>
                  </a>
                  <ul className="dropdown-menu">
                    <li className="header">You have 9 tasks</li>
                    <li>
                      { /* Inner menu: contains the tasks */ }
                      <ul className="menu">
                        <li>{ /* Task item */ }
                          <a href="#">
                            { /* Task title and progress text */ }
                            <h3>
                              Design some buttons
                              <small className="pull-right">20%</small>
                            </h3>
                            { /* The progress bar */ }
                            <div className="progress xs">
                              { /* Change the css width attribute to simulate progress */ }
                              <div className="progress-bar progress-bar-aqua" style={{width: "20%"}} role="progressbar" aria-valuenow="20" aria-valuemin="0" aria-valuemax="100">
                                <span className="sr-only">20% Complete</span>
                              </div>
                            </div>
                          </a>
                        </li>
                        { /* end task item */ }
                      </ul>
                    </li>
                    <li className="footer">
                      <a href="#">View all tasks</a>
                    </li>
                  </ul>
                </li>
                { /* User Account Menu */ }
                <li className="dropdown user user-menu">
                  { /* Menu Toggle Button */ }
                  <a href="#" className="dropdown-toggle" data-toggle="dropdown">
                    { /* The user image in the navbar*/ }
                    <img src="node_modules/admin-lte/dist/img/user2-160x160.jpg" className="user-image" alt="User Image" />
                    { /* hidden-xs hides the username on small devices so only the image appears. */ }
                    <span className="hidden-xs">Alexander Pierce</span>
                  </a>
                  <ul className="dropdown-menu">
                    { /* The user image in the menu */ }
                    <li className="user-header">
                      <img src="node_modules/admin-lte/dist/img/user2-160x160.jpg" className="img-circle" alt="User Image" />

                      <p>
                        Alexander Pierce - Web Developer
                        <small>Member since Nov. 2012</small>
                      </p>
                    </li>
                    { /* Menu Body */ }
                    <li className="user-body">
                      <div className="row">
                        <div className="col-xs-4 text-center">
                          <a href="#">Followers</a>
                        </div>
                        <div className="col-xs-4 text-center">
                          <a href="#">Sales</a>
                        </div>
                        <div className="col-xs-4 text-center">
                          <a href="#">Friends</a>
                        </div>
                      </div>
                      { /* /.row */ }
                    </li>
                    { /* Menu Footer*/ }
                    <li className="user-footer">
                      <div className="pull-left">
                        <a href="#" className="btn btn-default btn-flat">Profile</a>
                      </div>
                      <div className="pull-right">
                        <a href="#" className="btn btn-default btn-flat">Sign out</a>
                      </div>
                    </li>
                  </ul>
                </li>
                { /* Control Sidebar Toggle Button */ }
                <li>
                  <a href="#" data-toggle="control-sidebar"><i className="fa fa-gears"></i></a>
                </li>
              </ul>
            </div>
          </nav>
        </header>
        { /* Left side column. contains the logo and sidebar */ }
        <aside className="main-sidebar">

          { /* sidebar: style can be found in sidebar.less */ }
          <section className="sidebar">

            { /* Sidebar user panel (optional) */ }
            <div className="user-panel">
              <div className="pull-left image">
                <img src="node_modules/admin-lte/dist/img/user2-160x160.jpg" className="img-circle" alt="User Image" />
              </div>
              <div className="pull-left info">
                <p>Alexander Pierce</p>
                { /* Status */ }
                <a href="#"><i className="fa fa-circle text-success"></i> Online</a>
              </div>
            </div>

            { /* search form (Optional) */ }
            <form action="#" method="get" className="sidebar-form">
              <div className="input-group">
                <input type="text" name="q" className="form-control" placeholder="Search..." />
                    <span className="input-group-btn">
                      <button type="submit" name="search" id="search-btn" className="btn btn-flat"><i className="fa fa-search"></i>
                      </button>
                    </span>
              </div>
            </form>
            { /* /.search form */ }

            { /* Sidebar Menu */ }
            <ul className="sidebar-menu">
              <li className="header">HEADER</li>
              { /* Optionally, you can add icons to the links */ }
              <li><Link to="/release/config"><i className="fa fa-cog"></i> <span>Config</span></Link></li>
              <li><Link to="/release/list"><i className="fa fa-film"></i> <span>Movies</span></Link></li>
            </ul>
            { /* /.sidebar-menu */ }
          </section>
          { /* /.sidebar */ }
        </aside>

        { /* Content Wrapper. Contains page content */ }
        <div className="content-wrapper">
          {this.props.children}
        </div>
        { /* /.content-wrapper */ }

        { /* Main Footer */ }
        <footer className="main-footer">
          { /* To the right */ }
          <div className="pull-right hidden-xs">
            Anything you want
          </div>
          { /* Default to the left */ }
          <strong>Copyright &copy; 2015 <a href="#">Company</a>.</strong> All rights reserved.
        </footer>

        { /* Control Sidebar */ }
        <aside className="control-sidebar control-sidebar-dark">
          { /* Create the tabs */ }
          <ul className="nav nav-tabs nav-justified control-sidebar-tabs">
            <li className="active"><a href="#control-sidebar-home-tab" data-toggle="tab"><i className="fa fa-home"></i></a></li>
            <li><a href="#control-sidebar-settings-tab" data-toggle="tab"><i className="fa fa-gears"></i></a></li>
          </ul>
          { /* Tab panes */ }
          <div className="tab-content">
            { /* Home tab content */ }
            <div className="tab-pane active" id="control-sidebar-home-tab">
              <h3 className="control-sidebar-heading">Recent Activity</h3>
              <ul className="control-sidebar-menu">
                <li>
                  <a href="javascript::;">
                    <i className="menu-icon fa fa-birthday-cake bg-red"></i>

                    <div className="menu-info">
                      <h4 className="control-sidebar-subheading">Langdon Birthday</h4>

                      <p>Will be 23 on April 24th</p>
                    </div>
                  </a>
                </li>
              </ul>
              { /* /.control-sidebar-menu */ }

              <h3 className="control-sidebar-heading">Tasks Progress</h3>
              <ul className="control-sidebar-menu">
                <li>
                  <a href="javascript::;">
                    <h4 className="control-sidebar-subheading">
                      Custom Template Design
                      <span className="label label-danger pull-right">70%</span>
                    </h4>

                    <div className="progress progress-xxs">
                      <div className="progress-bar progress-bar-danger" style={{width: "70%"}}></div>
                    </div>
                  </a>
                </li>
              </ul>
              { /* /.control-sidebar-menu */ }

            </div>
            { /* /.tab-pane */ }
            { /* Stats tab content */ }
            <div className="tab-pane" id="control-sidebar-stats-tab">Stats Tab Content</div>
            { /* /.tab-pane */ }
            { /* Settings tab content */ }
            <div className="tab-pane" id="control-sidebar-settings-tab">
              <form method="post">
                <h3 className="control-sidebar-heading">General Settings</h3>

                <div className="form-group">
                  <label className="control-sidebar-subheading">
                    Report panel usage
                    <input type="checkbox" className="pull-right" defaultChecked={true} />
                  </label>

                  <p>
                    Some information about this general settings option
                  </p>
                </div>
                { /* /.form-group */ }
              </form>
            </div>
            { /* /.tab-pane */ }
          </div>
        </aside>
        { /* /.control-sidebar */ }
        { /* Add the sidebar's background. This div must be placed
             immediately after the control sidebar */ }
        <div className="control-sidebar-bg"></div>
      </div>
    )
  }
}
