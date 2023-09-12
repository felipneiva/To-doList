import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './App.css';

function App() {
  const [showModal, setShowModal] = useState(false);
  const [title, setTitle] = useState('');
  const [description, setDescription] = useState('');
  const [todos, setTodos] = useState([]);
  const [doneTodos, setDoneTodos] = useState([]);

  useEffect(() => {
    axios.get('http://localhost:8000/todo/undone')
    .then((res) => {
      setTodos(res.data);
    })
    .catch((err) => {
      console.log(err);
    })
  }, [])

  useEffect(() => {
    axios.get('http://localhost:8000/todo/done')
    .then((res) => {
      setDoneTodos(res.data);
    })
    .catch((err) => {
      console.log(err);
    })
  }, [])

  const handleOpenModal = () => {
    setShowModal(true);
  };

  const handleCloseModal = () => {
    setShowModal(false);
  };

  const handleAddTask = () => {
    axios.post('http://localhost:8000/todo', {title: title, description: description})
    .then((res) => {
      setTodos([...todos, res.data]);
    })
    .catch((err) => {
      console.log(err);
    })

    setTitle('');
    setDescription('');
    setShowModal(false);
  };

  const handleDeleteTask = (title) => {
    axios.delete(`http://localhost:8000/todo/${title}`)
    .then(() => {
      setTodos(todos.filter((todo) => todo.title !== title));
      setDoneTodos(doneTodos.filter((todo) => todo.title !== title));
    })
    .catch((err) => {
      console.log(err);
    })
  };

  const handleToggleTaskStatus = (title, isDone) => {
    axios.put(`http://localhost:8000/todo/${title}/toggle-status`)
      .then((res) => {
        if (isDone) {
          setDoneTodos([...doneTodos, res.data]);
          setTodos(todos.filter((todo) => todo.title !== title));
        } else {
          setTodos([...todos, res.data]);
          setDoneTodos(doneTodos.filter((todo) => todo.title !== title));
        }
      })
      .catch((err) => {
        console.log(err);
      });
  }
  

  return (
    <body>
    <div className='container'>
      <h1>To-Do List</h1>
      <button className = 'new-task' onClick={handleOpenModal}>New Task</button>
      {showModal && (
        <div className = 'add-task'>
          <input className='task-input' type='text' placeholder='Title' value={title} onChange={(e) => setTitle(e.target.value)}  
          onFocus={(e) => e.target.placeholder = ''} onBlur={(e) => e.target.placeholder = 'Title'} />
          <br />
          <input className='task-input' type='text' placeholder='Description' value={description} onChange={(e) => setDescription(e.target.value)} 
          onFocus={(e) => e.target.placeholder = ''} onBlur={(e) => e.target.placeholder = 'Description'} />
          <br />
          <button className = 'create-task' type='submit' onClick={handleAddTask}>Create</button>
          <button className = 'close' onClick={handleCloseModal}>Close</button>
        </div>
        )}
      <div className='tasks-container'>
      <div className='undone-tasks'>
      {todos.map((todo, index) => (
        <div key={index} className='todo-item'>
          <h2>{todo.title}</h2>
          <p>- {todo.description}</p>
          <button className='toggle-status' onClick={() => handleToggleTaskStatus(todo.title, true)}>Done</button>
          {<button className='delete' onClick={() => handleDeleteTask(todo.title)}>Delete</button>}
        </div>
      ))}
      </div>
      <div className='done-tasks'>
      {doneTodos.map((todo, index) => (
        <div key={index} className='done-item'>
          <h2>{todo.title}</h2>
          <p>- {todo.description}</p>
          <button className='toggle-status' onClick={() => handleToggleTaskStatus(todo.title, false)}>Undone</button>
          <button className='delete' onClick={() => handleDeleteTask(todo.title)}>Delete</button>
        </div>
      ))}
      </div>
      </div>
    </div>
    </body>
  );
}

export default App;

