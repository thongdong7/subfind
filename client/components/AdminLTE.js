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
            <span className="logo-mini"><b>S</b>F</span>
            { /* logo for regular state and mobile devices */ }
            <span className="logo-lg"><b>Sub</b>Find</span>
          </a>

          { /* Header Navbar */ }
          <nav className="navbar navbar-static-top" role="navigation">
            { /* Sidebar toggle button*/ }
            <a href="#" className="sidebar-toggle" data-toggle="offcanvas" role="button">
              <span className="sr-only">Toggle navigation</span>
            </a>
          </nav>
        </header>
        { /* Left side column. contains the logo and sidebar */ }
        <aside className="main-sidebar">

          <section className="sidebar">
            <ul className="sidebar-menu">
              <li><Link to="/release/config"><i className="fa fa-cog"></i> <span>Config</span></Link></li>
              <li><Link to="/release/list"><i className="fa fa-film"></i> <span>Movies</span></Link></li>
            </ul>
          </section>
        </aside>

        <div className="content-wrapper">
          {this.props.children}
        </div>

        <footer className="main-footer">
          <div className="pull-right hidden-xs">
            Anything you want
          </div>
          <strong>Copyright &copy; 2015 <a href="#">Company</a>.</strong> All rights reserved.
        </footer>
      </div>
    )
  }
}
