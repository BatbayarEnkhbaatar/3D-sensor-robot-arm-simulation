// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from yaskawa_msgs:action/YaskawaTasks.idl
// generated code does not contain a copyright notice

#ifndef YASKAWA_MSGS__ACTION__DETAIL__YASKAWA_TASKS__BUILDER_HPP_
#define YASKAWA_MSGS__ACTION__DETAIL__YASKAWA_TASKS__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "yaskawa_msgs/action/detail/yaskawa_tasks__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace yaskawa_msgs
{

namespace action
{

namespace builder
{

class Init_YaskawaTasks_Goal_task_number
{
public:
  Init_YaskawaTasks_Goal_task_number()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  ::yaskawa_msgs::action::YaskawaTasks_Goal task_number(::yaskawa_msgs::action::YaskawaTasks_Goal::_task_number_type arg)
  {
    msg_.task_number = std::move(arg);
    return std::move(msg_);
  }

private:
  ::yaskawa_msgs::action::YaskawaTasks_Goal msg_;
};

}  // namespace builder

}  // namespace action

template<typename MessageType>
auto build();

template<>
inline
auto build<::yaskawa_msgs::action::YaskawaTasks_Goal>()
{
  return yaskawa_msgs::action::builder::Init_YaskawaTasks_Goal_task_number();
}

}  // namespace yaskawa_msgs


namespace yaskawa_msgs
{

namespace action
{

namespace builder
{

class Init_YaskawaTasks_Result_success
{
public:
  Init_YaskawaTasks_Result_success()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  ::yaskawa_msgs::action::YaskawaTasks_Result success(::yaskawa_msgs::action::YaskawaTasks_Result::_success_type arg)
  {
    msg_.success = std::move(arg);
    return std::move(msg_);
  }

private:
  ::yaskawa_msgs::action::YaskawaTasks_Result msg_;
};

}  // namespace builder

}  // namespace action

template<typename MessageType>
auto build();

template<>
inline
auto build<::yaskawa_msgs::action::YaskawaTasks_Result>()
{
  return yaskawa_msgs::action::builder::Init_YaskawaTasks_Result_success();
}

}  // namespace yaskawa_msgs


namespace yaskawa_msgs
{

namespace action
{

namespace builder
{

class Init_YaskawaTasks_Feedback_percentage
{
public:
  Init_YaskawaTasks_Feedback_percentage()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  ::yaskawa_msgs::action::YaskawaTasks_Feedback percentage(::yaskawa_msgs::action::YaskawaTasks_Feedback::_percentage_type arg)
  {
    msg_.percentage = std::move(arg);
    return std::move(msg_);
  }

private:
  ::yaskawa_msgs::action::YaskawaTasks_Feedback msg_;
};

}  // namespace builder

}  // namespace action

template<typename MessageType>
auto build();

template<>
inline
auto build<::yaskawa_msgs::action::YaskawaTasks_Feedback>()
{
  return yaskawa_msgs::action::builder::Init_YaskawaTasks_Feedback_percentage();
}

}  // namespace yaskawa_msgs


namespace yaskawa_msgs
{

namespace action
{

namespace builder
{

class Init_YaskawaTasks_SendGoal_Request_goal
{
public:
  explicit Init_YaskawaTasks_SendGoal_Request_goal(::yaskawa_msgs::action::YaskawaTasks_SendGoal_Request & msg)
  : msg_(msg)
  {}
  ::yaskawa_msgs::action::YaskawaTasks_SendGoal_Request goal(::yaskawa_msgs::action::YaskawaTasks_SendGoal_Request::_goal_type arg)
  {
    msg_.goal = std::move(arg);
    return std::move(msg_);
  }

private:
  ::yaskawa_msgs::action::YaskawaTasks_SendGoal_Request msg_;
};

class Init_YaskawaTasks_SendGoal_Request_goal_id
{
public:
  Init_YaskawaTasks_SendGoal_Request_goal_id()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_YaskawaTasks_SendGoal_Request_goal goal_id(::yaskawa_msgs::action::YaskawaTasks_SendGoal_Request::_goal_id_type arg)
  {
    msg_.goal_id = std::move(arg);
    return Init_YaskawaTasks_SendGoal_Request_goal(msg_);
  }

private:
  ::yaskawa_msgs::action::YaskawaTasks_SendGoal_Request msg_;
};

}  // namespace builder

}  // namespace action

template<typename MessageType>
auto build();

template<>
inline
auto build<::yaskawa_msgs::action::YaskawaTasks_SendGoal_Request>()
{
  return yaskawa_msgs::action::builder::Init_YaskawaTasks_SendGoal_Request_goal_id();
}

}  // namespace yaskawa_msgs


namespace yaskawa_msgs
{

namespace action
{

namespace builder
{

class Init_YaskawaTasks_SendGoal_Response_stamp
{
public:
  explicit Init_YaskawaTasks_SendGoal_Response_stamp(::yaskawa_msgs::action::YaskawaTasks_SendGoal_Response & msg)
  : msg_(msg)
  {}
  ::yaskawa_msgs::action::YaskawaTasks_SendGoal_Response stamp(::yaskawa_msgs::action::YaskawaTasks_SendGoal_Response::_stamp_type arg)
  {
    msg_.stamp = std::move(arg);
    return std::move(msg_);
  }

private:
  ::yaskawa_msgs::action::YaskawaTasks_SendGoal_Response msg_;
};

class Init_YaskawaTasks_SendGoal_Response_accepted
{
public:
  Init_YaskawaTasks_SendGoal_Response_accepted()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_YaskawaTasks_SendGoal_Response_stamp accepted(::yaskawa_msgs::action::YaskawaTasks_SendGoal_Response::_accepted_type arg)
  {
    msg_.accepted = std::move(arg);
    return Init_YaskawaTasks_SendGoal_Response_stamp(msg_);
  }

private:
  ::yaskawa_msgs::action::YaskawaTasks_SendGoal_Response msg_;
};

}  // namespace builder

}  // namespace action

template<typename MessageType>
auto build();

template<>
inline
auto build<::yaskawa_msgs::action::YaskawaTasks_SendGoal_Response>()
{
  return yaskawa_msgs::action::builder::Init_YaskawaTasks_SendGoal_Response_accepted();
}

}  // namespace yaskawa_msgs


namespace yaskawa_msgs
{

namespace action
{

namespace builder
{

class Init_YaskawaTasks_GetResult_Request_goal_id
{
public:
  Init_YaskawaTasks_GetResult_Request_goal_id()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  ::yaskawa_msgs::action::YaskawaTasks_GetResult_Request goal_id(::yaskawa_msgs::action::YaskawaTasks_GetResult_Request::_goal_id_type arg)
  {
    msg_.goal_id = std::move(arg);
    return std::move(msg_);
  }

private:
  ::yaskawa_msgs::action::YaskawaTasks_GetResult_Request msg_;
};

}  // namespace builder

}  // namespace action

template<typename MessageType>
auto build();

template<>
inline
auto build<::yaskawa_msgs::action::YaskawaTasks_GetResult_Request>()
{
  return yaskawa_msgs::action::builder::Init_YaskawaTasks_GetResult_Request_goal_id();
}

}  // namespace yaskawa_msgs


namespace yaskawa_msgs
{

namespace action
{

namespace builder
{

class Init_YaskawaTasks_GetResult_Response_result
{
public:
  explicit Init_YaskawaTasks_GetResult_Response_result(::yaskawa_msgs::action::YaskawaTasks_GetResult_Response & msg)
  : msg_(msg)
  {}
  ::yaskawa_msgs::action::YaskawaTasks_GetResult_Response result(::yaskawa_msgs::action::YaskawaTasks_GetResult_Response::_result_type arg)
  {
    msg_.result = std::move(arg);
    return std::move(msg_);
  }

private:
  ::yaskawa_msgs::action::YaskawaTasks_GetResult_Response msg_;
};

class Init_YaskawaTasks_GetResult_Response_status
{
public:
  Init_YaskawaTasks_GetResult_Response_status()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_YaskawaTasks_GetResult_Response_result status(::yaskawa_msgs::action::YaskawaTasks_GetResult_Response::_status_type arg)
  {
    msg_.status = std::move(arg);
    return Init_YaskawaTasks_GetResult_Response_result(msg_);
  }

private:
  ::yaskawa_msgs::action::YaskawaTasks_GetResult_Response msg_;
};

}  // namespace builder

}  // namespace action

template<typename MessageType>
auto build();

template<>
inline
auto build<::yaskawa_msgs::action::YaskawaTasks_GetResult_Response>()
{
  return yaskawa_msgs::action::builder::Init_YaskawaTasks_GetResult_Response_status();
}

}  // namespace yaskawa_msgs


namespace yaskawa_msgs
{

namespace action
{

namespace builder
{

class Init_YaskawaTasks_FeedbackMessage_feedback
{
public:
  explicit Init_YaskawaTasks_FeedbackMessage_feedback(::yaskawa_msgs::action::YaskawaTasks_FeedbackMessage & msg)
  : msg_(msg)
  {}
  ::yaskawa_msgs::action::YaskawaTasks_FeedbackMessage feedback(::yaskawa_msgs::action::YaskawaTasks_FeedbackMessage::_feedback_type arg)
  {
    msg_.feedback = std::move(arg);
    return std::move(msg_);
  }

private:
  ::yaskawa_msgs::action::YaskawaTasks_FeedbackMessage msg_;
};

class Init_YaskawaTasks_FeedbackMessage_goal_id
{
public:
  Init_YaskawaTasks_FeedbackMessage_goal_id()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_YaskawaTasks_FeedbackMessage_feedback goal_id(::yaskawa_msgs::action::YaskawaTasks_FeedbackMessage::_goal_id_type arg)
  {
    msg_.goal_id = std::move(arg);
    return Init_YaskawaTasks_FeedbackMessage_feedback(msg_);
  }

private:
  ::yaskawa_msgs::action::YaskawaTasks_FeedbackMessage msg_;
};

}  // namespace builder

}  // namespace action

template<typename MessageType>
auto build();

template<>
inline
auto build<::yaskawa_msgs::action::YaskawaTasks_FeedbackMessage>()
{
  return yaskawa_msgs::action::builder::Init_YaskawaTasks_FeedbackMessage_goal_id();
}

}  // namespace yaskawa_msgs

#endif  // YASKAWA_MSGS__ACTION__DETAIL__YASKAWA_TASKS__BUILDER_HPP_
