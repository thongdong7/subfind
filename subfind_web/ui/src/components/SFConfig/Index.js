// import React, { Component, PropTypes } from "react";
// import MovieFolder from "./MovieFolder";

// let mb = 1024 * 1024;

// const FormRow = ({ children }) => {
//   return (
//     <div className="row">
//       <div className="col-sm-3">
//         {children[0]}
//       </div>
//       <div className="col-sm-9">
//         {children[1]}
//       </div>
//     </div>
//   );
// };

// const builtinProviders = [
//   { name: "opensubtitles", displayName: "Opensubtitles" },
//   { name: "subscene", displayName: "Subscene" },
// ];

// class SFConfigIndex extends Component {
//   static contextTypes = {
//     router: PropTypes.object,
//   };

//   render() {
//     const {
//       config: { src: folders, lang: languages, providers, force, remove },
//     } = this.props;
//     // console.log('config', this.props.config);
//     const config = this.props.config;

//     return (
//       <div className="box box-solid">
//         <div className="box-header with-border">
//           <h3 className="box-title">
//             <tb.BackButton />
//           </h3>
//         </div>
//         <div className="box-body">
//           <div>
//             <FormRow>
//               <strong>Movie Folders</strong>
//               <div>
//                 {folders.map((folder, k) => {
//                   return (
//                     <MovieFolder src={folder} key={k}>
//                       <tb.APIActionButton
//                         name="Remove"
//                         icon="trash"
//                         hideName
//                         type="danger"
//                         action={[
//                           configActions.updateListField,
//                           "src",
//                           folder,
//                           false,
//                         ]}
//                       />
//                     </MovieFolder>
//                   );
//                 })}
//                 <tb.InputTextForm
//                   actionFunc={value => [
//                     configActions.updateListField,
//                     "src",
//                     value,
//                     true,
//                   ]}
//                 />
//               </div>
//             </FormRow>
//             <FormRow>
//               <strong>Languages</strong>
//               <div>
//                 {languages.map((lang, k) => {
//                   return (
//                     <MovieFolder src={lang} key={k}>
//                       <tb.APIActionButton
//                         name="Remove"
//                         icon="trash"
//                         hideName
//                         type="danger"
//                         action={[
//                           configActions.updateListField,
//                           "lang",
//                           lang,
//                           false,
//                         ]}
//                       />
//                     </MovieFolder>
//                   );
//                 })}

//                 <tb.InputTextForm
//                   actionFunc={value => [
//                     configActions.updateListField,
//                     "lang",
//                     value,
//                     true,
//                   ]}
//                 />
//               </div>
//             </FormRow>
//             <FormRow>
//               <strong>Providers</strong>
//               <div>
//                 {builtinProviders.map(
//                   ({ name: providerName, displayName }, k) => {
//                     let checked = providers.indexOf(providerName) >= 0;
//                     return (
//                       <div key={k}>
//                         <div className="col-sm-3">
//                           {displayName}
//                         </div>
//                         <div className="col-sm-9">
//                           <tb.APIActionSwitch
//                             checked={checked}
//                             action={[
//                               configActions.updateListField,
//                               "providers",
//                               providerName,
//                             ]}
//                           />
//                         </div>
//                       </div>
//                     );
//                   }
//                 )}
//               </div>
//             </FormRow>
//             <FormRow>
//               <strong>Force download subtitle</strong>
//               <tb.APIActionSwitch
//                 checked={force}
//                 action={[configActions.updateField, "force"]}
//               />
//             </FormRow>
//             <FormRow>
//               <strong>Remove old subtitles if not found new subtitle</strong>
//               <tb.APIActionSwitch
//                 checked={remove}
//                 action={[configActions.updateField, "remove"]}
//               />
//             </FormRow>
//             <FormRow>
//               <div>
//                 <strong>Min movie size (MB)</strong>
//                 <div>(to ignore sample videos)</div>
//               </div>
//               <div>
//                 <tb.InputInplace
//                   value={config["min-movie-size"] / mb}
//                   actionFunc={value => [
//                     configActions.updateField,
//                     "min-movie-size",
//                     Number(value) * mb,
//                   ]}
//                 />
//               </div>
//             </FormRow>
//             <FormRow>
//               <strong>Number subtitles</strong>
//               <tb.InputInplace
//                 value={config["max-sub"]}
//                 action={[configActions.updateField, "max-sub"]}
//               />
//             </FormRow>
//           </div>
//         </div>
//       </div>
//     );
//   }
// }

// // SFConfigIndex.contextTypes = {
// //     router: React.PropTypes.object
// // }

// export default tb.connect2({
//   start: dispatch => {
//     dispatch(configActions.load);
//   },
//   props: ({ config }, ownProps, dispatch) => ({
//     config,
//   }),
// })(SFConfigIndex);
