// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from yaskawa_msgs:action/YaskawaTasks.idl
// generated code does not contain a copyright notice

#ifndef YASKAWA_MSGS__ACTION__DETAIL__YASKAWA_TASKS__TRAITS_HPP_
#define YASKAWA_MSGS__ACTION__DETAIL__YASKAWA_TASKS__TRAITS_HPP_

#include <stdint.h>

#include <sstream>
#include <string>
#include <type_traits>

#include "yaskawa_msgs/action/detail/yaskawa_tasks__struct.hpp"
#include "rosidl_runtime_cpp/traits.hpp"

namespace yaskawa_msgs
{

namespace action
{

inline void to_flow_style_yaml(
  const YaskawaTasks_Goal & msg,
  std::ostream & out)
{
  out << "{";
  // member: task_number
  {
    out << "task_number: ";
    rosidl_generator_traits::value_to_yaml(msg.task_number, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const YaskawaTasks_Goal & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: task_number
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "task_number: ";
    rosidl_generator_traits::value_to_yaml(msg.task_number, out);
    out << "\n";
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const YaskawaTasks_Goal & msg, bool use_flow_style = false)
{
  std::ostringstream out;
  if (use_flow_style) {
    to_flow_style_yaml(msg, out);
  } else {
    to_block_style_yaml(msg, out);
  }
  return out.str();
}

}  // namespace action

}  // namespace yaskawa_msgs

namespace rosidl_generator_traits
{

[[deprecated("use yaskawa_msgs::action::to_block_style_yaml() instead")]]
inline void to_yaml(
  const yaskawa_msgs::action::YaskawaTasks_Goal & msg,
  std::ostream & out, size_t indentation = 0)
{
  yaskawa_msgs::action::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use yaskawa_msgs::action::to_yaml() instead")]]
inline std::string to_yaml(const yaskawa_msgs::action::YaskawaTasks_Goal & msg)
{
  return yaskawa_msgs::action::to_yaml(msg);
}

template<>
inline const char * data_type<yaskawa_msgs::action::YaskawaTasks_Goal>()
{
  return "yaskawa_msgs::action::YaskawaTasks_Goal";
}

template<>
inline const char * name<yaskawa_msgs::action::YaskawaTasks_Goal>()
{
  return "yaskawa_msgs/action/YaskawaTasks_Goal";
}

template<>
struct has_fixed_size<yaskawa_msgs::action::YaskawaTasks_Goal>
  : std::integral_constant<bool, true> {};

template<>
struct has_bounded_size<yaskawa_msgs::action::YaskawaTasks_Goal>
  : std::integral_constant<bool, true> {};

template<>
struct is_message<yaskawa_msgs::action::YaskawaTasks_Goal>
  : std::true_type {};

}  // namespace rosidl_generator_traits

namespace yaskawa_msgs
{

namespace action
{

inline void to_flow_style_yaml(
  const YaskawaTasks_Result & msg,
  std::ostream & out)
{
  out << "{";
  // member: success
  {
    out << "success: ";
    rosidl_generator_traits::value_to_yaml(msg.success, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const YaskawaTasks_Result & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: success
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "success: ";
    rosidl_generator_traits::value_to_yaml(msg.success, out);
    out << "\n";
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const YaskawaTasks_Result & msg, bool use_flow_style = false)
{
  std::ostringstream out;
  if (use_flow_style) {
    to_flow_style_yaml(msg, out);
  } else {
    to_block_style_yaml(msg, out);
  }
  return out.str();
}

}  // namespace action

}  // namespace yaskawa_msgs

namespace rosidl_generator_traits
{

[[deprecated("use yaskawa_msgs::action::to_block_style_yaml() instead")]]
inline void to_yaml(
  const yaskawa_msgs::action::YaskawaTasks_Result & msg,
  std::ostream & out, size_t indentation = 0)
{
  yaskawa_msgs::action::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use yaskawa_msgs::action::to_yaml() instead")]]
inline std::string to_yaml(const yaskawa_msgs::action::YaskawaTasks_Result & msg)
{
  return yaskawa_msgs::action::to_yaml(msg);
}

template<>
inline const char * data_type<yaskawa_msgs::action::YaskawaTasks_Result>()
{
  return "yaskawa_msgs::action::YaskawaTasks_Result";
}

template<>
inline const char * name<yaskawa_msgs::action::YaskawaTasks_Result>()
{
  return "yaskawa_msgs/action/YaskawaTasks_Result";
}

template<>
struct has_fixed_size<yaskawa_msgs::action::YaskawaTasks_Result>
  : std::integral_constant<bool, true> {};

template<>
struct has_bounded_size<yaskawa_msgs::action::YaskawaTasks_Result>
  : std::integral_constant<bool, true> {};

template<>
struct is_message<yaskawa_msgs::action::YaskawaTasks_Result>
  : std::true_type {};

}  // namespace rosidl_generator_traits

namespace yaskawa_msgs
{

namespace action
{

inline void to_flow_style_yaml(
  const YaskawaTasks_Feedback & msg,
  std::ostream & out)
{
  out << "{";
  // member: percentage
  {
    out << "percentage: ";
    rosidl_generator_traits::value_to_yaml(msg.percentage, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const YaskawaTasks_Feedback & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: percentage
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "percentage: ";
    rosidl_generator_traits::value_to_yaml(msg.percentage, out);
    out << "\n";
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const YaskawaTasks_Feedback & msg, bool use_flow_style = false)
{
  std::ostringstream out;
  if (use_flow_style) {
    to_flow_style_yaml(msg, out);
  } else {
    to_block_style_yaml(msg, out);
  }
  return out.str();
}

}  // namespace action

}  // namespace yaskawa_msgs

namespace rosidl_generator_traits
{

[[deprecated("use yaskawa_msgs::action::to_block_style_yaml() instead")]]
inline void to_yaml(
  const yaskawa_msgs::action::YaskawaTasks_Feedback & msg,
  std::ostream & out, size_t indentation = 0)
{
  yaskawa_msgs::action::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use yaskawa_msgs::action::to_yaml() instead")]]
inline std::string to_yaml(const yaskawa_msgs::action::YaskawaTasks_Feedback & msg)
{
  return yaskawa_msgs::action::to_yaml(msg);
}

template<>
inline const char * data_type<yaskawa_msgs::action::YaskawaTasks_Feedback>()
{
  return "yaskawa_msgs::action::YaskawaTasks_Feedback";
}

template<>
inline const char * name<yaskawa_msgs::action::YaskawaTasks_Feedback>()
{
  return "yaskawa_msgs/action/YaskawaTasks_Feedback";
}

template<>
struct has_fixed_size<yaskawa_msgs::action::YaskawaTasks_Feedback>
  : std::integral_constant<bool, true> {};

template<>
struct has_bounded_size<yaskawa_msgs::action::YaskawaTasks_Feedback>
  : std::integral_constant<bool, true> {};

template<>
struct is_message<yaskawa_msgs::action::YaskawaTasks_Feedback>
  : std::true_type {};

}  // namespace rosidl_generator_traits

// Include directives for member types
// Member 'goal_id'
#include "unique_identifier_msgs/msg/detail/uuid__traits.hpp"
// Member 'goal'
#include "yaskawa_msgs/action/detail/yaskawa_tasks__traits.hpp"

namespace yaskawa_msgs
{

namespace action
{

inline void to_flow_style_yaml(
  const YaskawaTasks_SendGoal_Request & msg,
  std::ostream & out)
{
  out << "{";
  // member: goal_id
  {
    out << "goal_id: ";
    to_flow_style_yaml(msg.goal_id, out);
    out << ", ";
  }

  // member: goal
  {
    out << "goal: ";
    to_flow_style_yaml(msg.goal, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const YaskawaTasks_SendGoal_Request & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: goal_id
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "goal_id:\n";
    to_block_style_yaml(msg.goal_id, out, indentation + 2);
  }

  // member: goal
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "goal:\n";
    to_block_style_yaml(msg.goal, out, indentation + 2);
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const YaskawaTasks_SendGoal_Request & msg, bool use_flow_style = false)
{
  std::ostringstream out;
  if (use_flow_style) {
    to_flow_style_yaml(msg, out);
  } else {
    to_block_style_yaml(msg, out);
  }
  return out.str();
}

}  // namespace action

}  // namespace yaskawa_msgs

namespace rosidl_generator_traits
{

[[deprecated("use yaskawa_msgs::action::to_block_style_yaml() instead")]]
inline void to_yaml(
  const yaskawa_msgs::action::YaskawaTasks_SendGoal_Request & msg,
  std::ostream & out, size_t indentation = 0)
{
  yaskawa_msgs::action::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use yaskawa_msgs::action::to_yaml() instead")]]
inline std::string to_yaml(const yaskawa_msgs::action::YaskawaTasks_SendGoal_Request & msg)
{
  return yaskawa_msgs::action::to_yaml(msg);
}

template<>
inline const char * data_type<yaskawa_msgs::action::YaskawaTasks_SendGoal_Request>()
{
  return "yaskawa_msgs::action::YaskawaTasks_SendGoal_Request";
}

template<>
inline const char * name<yaskawa_msgs::action::YaskawaTasks_SendGoal_Request>()
{
  return "yaskawa_msgs/action/YaskawaTasks_SendGoal_Request";
}

template<>
struct has_fixed_size<yaskawa_msgs::action::YaskawaTasks_SendGoal_Request>
  : std::integral_constant<bool, has_fixed_size<unique_identifier_msgs::msg::UUID>::value && has_fixed_size<yaskawa_msgs::action::YaskawaTasks_Goal>::value> {};

template<>
struct has_bounded_size<yaskawa_msgs::action::YaskawaTasks_SendGoal_Request>
  : std::integral_constant<bool, has_bounded_size<unique_identifier_msgs::msg::UUID>::value && has_bounded_size<yaskawa_msgs::action::YaskawaTasks_Goal>::value> {};

template<>
struct is_message<yaskawa_msgs::action::YaskawaTasks_SendGoal_Request>
  : std::true_type {};

}  // namespace rosidl_generator_traits

// Include directives for member types
// Member 'stamp'
#include "builtin_interfaces/msg/detail/time__traits.hpp"

namespace yaskawa_msgs
{

namespace action
{

inline void to_flow_style_yaml(
  const YaskawaTasks_SendGoal_Response & msg,
  std::ostream & out)
{
  out << "{";
  // member: accepted
  {
    out << "accepted: ";
    rosidl_generator_traits::value_to_yaml(msg.accepted, out);
    out << ", ";
  }

  // member: stamp
  {
    out << "stamp: ";
    to_flow_style_yaml(msg.stamp, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const YaskawaTasks_SendGoal_Response & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: accepted
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "accepted: ";
    rosidl_generator_traits::value_to_yaml(msg.accepted, out);
    out << "\n";
  }

  // member: stamp
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "stamp:\n";
    to_block_style_yaml(msg.stamp, out, indentation + 2);
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const YaskawaTasks_SendGoal_Response & msg, bool use_flow_style = false)
{
  std::ostringstream out;
  if (use_flow_style) {
    to_flow_style_yaml(msg, out);
  } else {
    to_block_style_yaml(msg, out);
  }
  return out.str();
}

}  // namespace action

}  // namespace yaskawa_msgs

namespace rosidl_generator_traits
{

[[deprecated("use yaskawa_msgs::action::to_block_style_yaml() instead")]]
inline void to_yaml(
  const yaskawa_msgs::action::YaskawaTasks_SendGoal_Response & msg,
  std::ostream & out, size_t indentation = 0)
{
  yaskawa_msgs::action::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use yaskawa_msgs::action::to_yaml() instead")]]
inline std::string to_yaml(const yaskawa_msgs::action::YaskawaTasks_SendGoal_Response & msg)
{
  return yaskawa_msgs::action::to_yaml(msg);
}

template<>
inline const char * data_type<yaskawa_msgs::action::YaskawaTasks_SendGoal_Response>()
{
  return "yaskawa_msgs::action::YaskawaTasks_SendGoal_Response";
}

template<>
inline const char * name<yaskawa_msgs::action::YaskawaTasks_SendGoal_Response>()
{
  return "yaskawa_msgs/action/YaskawaTasks_SendGoal_Response";
}

template<>
struct has_fixed_size<yaskawa_msgs::action::YaskawaTasks_SendGoal_Response>
  : std::integral_constant<bool, has_fixed_size<builtin_interfaces::msg::Time>::value> {};

template<>
struct has_bounded_size<yaskawa_msgs::action::YaskawaTasks_SendGoal_Response>
  : std::integral_constant<bool, has_bounded_size<builtin_interfaces::msg::Time>::value> {};

template<>
struct is_message<yaskawa_msgs::action::YaskawaTasks_SendGoal_Response>
  : std::true_type {};

}  // namespace rosidl_generator_traits

namespace rosidl_generator_traits
{

template<>
inline const char * data_type<yaskawa_msgs::action::YaskawaTasks_SendGoal>()
{
  return "yaskawa_msgs::action::YaskawaTasks_SendGoal";
}

template<>
inline const char * name<yaskawa_msgs::action::YaskawaTasks_SendGoal>()
{
  return "yaskawa_msgs/action/YaskawaTasks_SendGoal";
}

template<>
struct has_fixed_size<yaskawa_msgs::action::YaskawaTasks_SendGoal>
  : std::integral_constant<
    bool,
    has_fixed_size<yaskawa_msgs::action::YaskawaTasks_SendGoal_Request>::value &&
    has_fixed_size<yaskawa_msgs::action::YaskawaTasks_SendGoal_Response>::value
  >
{
};

template<>
struct has_bounded_size<yaskawa_msgs::action::YaskawaTasks_SendGoal>
  : std::integral_constant<
    bool,
    has_bounded_size<yaskawa_msgs::action::YaskawaTasks_SendGoal_Request>::value &&
    has_bounded_size<yaskawa_msgs::action::YaskawaTasks_SendGoal_Response>::value
  >
{
};

template<>
struct is_service<yaskawa_msgs::action::YaskawaTasks_SendGoal>
  : std::true_type
{
};

template<>
struct is_service_request<yaskawa_msgs::action::YaskawaTasks_SendGoal_Request>
  : std::true_type
{
};

template<>
struct is_service_response<yaskawa_msgs::action::YaskawaTasks_SendGoal_Response>
  : std::true_type
{
};

}  // namespace rosidl_generator_traits

// Include directives for member types
// Member 'goal_id'
// already included above
// #include "unique_identifier_msgs/msg/detail/uuid__traits.hpp"

namespace yaskawa_msgs
{

namespace action
{

inline void to_flow_style_yaml(
  const YaskawaTasks_GetResult_Request & msg,
  std::ostream & out)
{
  out << "{";
  // member: goal_id
  {
    out << "goal_id: ";
    to_flow_style_yaml(msg.goal_id, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const YaskawaTasks_GetResult_Request & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: goal_id
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "goal_id:\n";
    to_block_style_yaml(msg.goal_id, out, indentation + 2);
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const YaskawaTasks_GetResult_Request & msg, bool use_flow_style = false)
{
  std::ostringstream out;
  if (use_flow_style) {
    to_flow_style_yaml(msg, out);
  } else {
    to_block_style_yaml(msg, out);
  }
  return out.str();
}

}  // namespace action

}  // namespace yaskawa_msgs

namespace rosidl_generator_traits
{

[[deprecated("use yaskawa_msgs::action::to_block_style_yaml() instead")]]
inline void to_yaml(
  const yaskawa_msgs::action::YaskawaTasks_GetResult_Request & msg,
  std::ostream & out, size_t indentation = 0)
{
  yaskawa_msgs::action::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use yaskawa_msgs::action::to_yaml() instead")]]
inline std::string to_yaml(const yaskawa_msgs::action::YaskawaTasks_GetResult_Request & msg)
{
  return yaskawa_msgs::action::to_yaml(msg);
}

template<>
inline const char * data_type<yaskawa_msgs::action::YaskawaTasks_GetResult_Request>()
{
  return "yaskawa_msgs::action::YaskawaTasks_GetResult_Request";
}

template<>
inline const char * name<yaskawa_msgs::action::YaskawaTasks_GetResult_Request>()
{
  return "yaskawa_msgs/action/YaskawaTasks_GetResult_Request";
}

template<>
struct has_fixed_size<yaskawa_msgs::action::YaskawaTasks_GetResult_Request>
  : std::integral_constant<bool, has_fixed_size<unique_identifier_msgs::msg::UUID>::value> {};

template<>
struct has_bounded_size<yaskawa_msgs::action::YaskawaTasks_GetResult_Request>
  : std::integral_constant<bool, has_bounded_size<unique_identifier_msgs::msg::UUID>::value> {};

template<>
struct is_message<yaskawa_msgs::action::YaskawaTasks_GetResult_Request>
  : std::true_type {};

}  // namespace rosidl_generator_traits

// Include directives for member types
// Member 'result'
// already included above
// #include "yaskawa_msgs/action/detail/yaskawa_tasks__traits.hpp"

namespace yaskawa_msgs
{

namespace action
{

inline void to_flow_style_yaml(
  const YaskawaTasks_GetResult_Response & msg,
  std::ostream & out)
{
  out << "{";
  // member: status
  {
    out << "status: ";
    rosidl_generator_traits::value_to_yaml(msg.status, out);
    out << ", ";
  }

  // member: result
  {
    out << "result: ";
    to_flow_style_yaml(msg.result, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const YaskawaTasks_GetResult_Response & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: status
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "status: ";
    rosidl_generator_traits::value_to_yaml(msg.status, out);
    out << "\n";
  }

  // member: result
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "result:\n";
    to_block_style_yaml(msg.result, out, indentation + 2);
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const YaskawaTasks_GetResult_Response & msg, bool use_flow_style = false)
{
  std::ostringstream out;
  if (use_flow_style) {
    to_flow_style_yaml(msg, out);
  } else {
    to_block_style_yaml(msg, out);
  }
  return out.str();
}

}  // namespace action

}  // namespace yaskawa_msgs

namespace rosidl_generator_traits
{

[[deprecated("use yaskawa_msgs::action::to_block_style_yaml() instead")]]
inline void to_yaml(
  const yaskawa_msgs::action::YaskawaTasks_GetResult_Response & msg,
  std::ostream & out, size_t indentation = 0)
{
  yaskawa_msgs::action::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use yaskawa_msgs::action::to_yaml() instead")]]
inline std::string to_yaml(const yaskawa_msgs::action::YaskawaTasks_GetResult_Response & msg)
{
  return yaskawa_msgs::action::to_yaml(msg);
}

template<>
inline const char * data_type<yaskawa_msgs::action::YaskawaTasks_GetResult_Response>()
{
  return "yaskawa_msgs::action::YaskawaTasks_GetResult_Response";
}

template<>
inline const char * name<yaskawa_msgs::action::YaskawaTasks_GetResult_Response>()
{
  return "yaskawa_msgs/action/YaskawaTasks_GetResult_Response";
}

template<>
struct has_fixed_size<yaskawa_msgs::action::YaskawaTasks_GetResult_Response>
  : std::integral_constant<bool, has_fixed_size<yaskawa_msgs::action::YaskawaTasks_Result>::value> {};

template<>
struct has_bounded_size<yaskawa_msgs::action::YaskawaTasks_GetResult_Response>
  : std::integral_constant<bool, has_bounded_size<yaskawa_msgs::action::YaskawaTasks_Result>::value> {};

template<>
struct is_message<yaskawa_msgs::action::YaskawaTasks_GetResult_Response>
  : std::true_type {};

}  // namespace rosidl_generator_traits

namespace rosidl_generator_traits
{

template<>
inline const char * data_type<yaskawa_msgs::action::YaskawaTasks_GetResult>()
{
  return "yaskawa_msgs::action::YaskawaTasks_GetResult";
}

template<>
inline const char * name<yaskawa_msgs::action::YaskawaTasks_GetResult>()
{
  return "yaskawa_msgs/action/YaskawaTasks_GetResult";
}

template<>
struct has_fixed_size<yaskawa_msgs::action::YaskawaTasks_GetResult>
  : std::integral_constant<
    bool,
    has_fixed_size<yaskawa_msgs::action::YaskawaTasks_GetResult_Request>::value &&
    has_fixed_size<yaskawa_msgs::action::YaskawaTasks_GetResult_Response>::value
  >
{
};

template<>
struct has_bounded_size<yaskawa_msgs::action::YaskawaTasks_GetResult>
  : std::integral_constant<
    bool,
    has_bounded_size<yaskawa_msgs::action::YaskawaTasks_GetResult_Request>::value &&
    has_bounded_size<yaskawa_msgs::action::YaskawaTasks_GetResult_Response>::value
  >
{
};

template<>
struct is_service<yaskawa_msgs::action::YaskawaTasks_GetResult>
  : std::true_type
{
};

template<>
struct is_service_request<yaskawa_msgs::action::YaskawaTasks_GetResult_Request>
  : std::true_type
{
};

template<>
struct is_service_response<yaskawa_msgs::action::YaskawaTasks_GetResult_Response>
  : std::true_type
{
};

}  // namespace rosidl_generator_traits

// Include directives for member types
// Member 'goal_id'
// already included above
// #include "unique_identifier_msgs/msg/detail/uuid__traits.hpp"
// Member 'feedback'
// already included above
// #include "yaskawa_msgs/action/detail/yaskawa_tasks__traits.hpp"

namespace yaskawa_msgs
{

namespace action
{

inline void to_flow_style_yaml(
  const YaskawaTasks_FeedbackMessage & msg,
  std::ostream & out)
{
  out << "{";
  // member: goal_id
  {
    out << "goal_id: ";
    to_flow_style_yaml(msg.goal_id, out);
    out << ", ";
  }

  // member: feedback
  {
    out << "feedback: ";
    to_flow_style_yaml(msg.feedback, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const YaskawaTasks_FeedbackMessage & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: goal_id
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "goal_id:\n";
    to_block_style_yaml(msg.goal_id, out, indentation + 2);
  }

  // member: feedback
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "feedback:\n";
    to_block_style_yaml(msg.feedback, out, indentation + 2);
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const YaskawaTasks_FeedbackMessage & msg, bool use_flow_style = false)
{
  std::ostringstream out;
  if (use_flow_style) {
    to_flow_style_yaml(msg, out);
  } else {
    to_block_style_yaml(msg, out);
  }
  return out.str();
}

}  // namespace action

}  // namespace yaskawa_msgs

namespace rosidl_generator_traits
{

[[deprecated("use yaskawa_msgs::action::to_block_style_yaml() instead")]]
inline void to_yaml(
  const yaskawa_msgs::action::YaskawaTasks_FeedbackMessage & msg,
  std::ostream & out, size_t indentation = 0)
{
  yaskawa_msgs::action::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use yaskawa_msgs::action::to_yaml() instead")]]
inline std::string to_yaml(const yaskawa_msgs::action::YaskawaTasks_FeedbackMessage & msg)
{
  return yaskawa_msgs::action::to_yaml(msg);
}

template<>
inline const char * data_type<yaskawa_msgs::action::YaskawaTasks_FeedbackMessage>()
{
  return "yaskawa_msgs::action::YaskawaTasks_FeedbackMessage";
}

template<>
inline const char * name<yaskawa_msgs::action::YaskawaTasks_FeedbackMessage>()
{
  return "yaskawa_msgs/action/YaskawaTasks_FeedbackMessage";
}

template<>
struct has_fixed_size<yaskawa_msgs::action::YaskawaTasks_FeedbackMessage>
  : std::integral_constant<bool, has_fixed_size<unique_identifier_msgs::msg::UUID>::value && has_fixed_size<yaskawa_msgs::action::YaskawaTasks_Feedback>::value> {};

template<>
struct has_bounded_size<yaskawa_msgs::action::YaskawaTasks_FeedbackMessage>
  : std::integral_constant<bool, has_bounded_size<unique_identifier_msgs::msg::UUID>::value && has_bounded_size<yaskawa_msgs::action::YaskawaTasks_Feedback>::value> {};

template<>
struct is_message<yaskawa_msgs::action::YaskawaTasks_FeedbackMessage>
  : std::true_type {};

}  // namespace rosidl_generator_traits


namespace rosidl_generator_traits
{

template<>
struct is_action<yaskawa_msgs::action::YaskawaTasks>
  : std::true_type
{
};

template<>
struct is_action_goal<yaskawa_msgs::action::YaskawaTasks_Goal>
  : std::true_type
{
};

template<>
struct is_action_result<yaskawa_msgs::action::YaskawaTasks_Result>
  : std::true_type
{
};

template<>
struct is_action_feedback<yaskawa_msgs::action::YaskawaTasks_Feedback>
  : std::true_type
{
};

}  // namespace rosidl_generator_traits


#endif  // YASKAWA_MSGS__ACTION__DETAIL__YASKAWA_TASKS__TRAITS_HPP_
