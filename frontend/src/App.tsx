import { useState } from 'react'
import './App.css'
import type { Problem } from './types/Problem'
import ProblemRow from './components/ProblemRow'

// Sample data - in a real app, this would come from an API or database
const sampleProblems: Problem[] = [
  {
    id: 1,
    number: 1,
    name: "Two Sum",
    description: "Given an array of integers nums and an integer target, return indices of the two numbers such that they add up to target.",
    difficulty: "Easy",
    category: "Array & Hashing",
    solution: "Use a hash map to store complements",
    approach: "Hash Map",
    timeComplexity: "O(n)",
    spaceComplexity: "O(n)",
    dateSolved: "2024-03-20",
    status: "Solved",
    notes: "Classic hash map problem"
  },
  {
    id: 2,
    number: 2,
    name: "Add Two Numbers",
    description: "You are given two non-empty linked lists representing two non-negative integers. The digits are stored in reverse order, and each of their nodes contains a single digit.",
    difficulty: "Medium",
    category: "Linked List",
    solution: "Simulate addition with carry",
    approach: "Linked List Traversal",
    timeComplexity: "O(max(n,m))",
    spaceComplexity: "O(max(n,m))",
    dateSolved: "2024-03-19",
    status: "Solved",
    notes: "Watch out for carry at the end"
  }
];

function App() {
  const [problems, _setProblems] = useState<Problem[]>(sampleProblems);
  const [filter, setFilter] = useState({
    difficulty: 'All',
    status: 'All',
    category: 'All'
  });

  const filteredProblems = problems.filter(problem => {
    return (filter.difficulty === 'All' || problem.difficulty === filter.difficulty) &&
           (filter.status === 'All' || problem.status === filter.status) &&
           (filter.category === 'All' || problem.category === filter.category);
  });

  return (
    <div className="app">
      <header className="app-header">
        <h1>LeetVault</h1>
        <p>Track your LeetCode progress</p>
      </header>

      <div className="dashboard">
        <div className="filters">
          <select 
            value={filter.difficulty}
            onChange={(e) => setFilter({...filter, difficulty: e.target.value})}
          >
            <option value="All">All Difficulties</option>
            <option value="Easy">Easy</option>
            <option value="Medium">Medium</option>
            <option value="Hard">Hard</option>
          </select>

          <select 
            value={filter.status}
            onChange={(e) => setFilter({...filter, status: e.target.value})}
          >
            <option value="All">All Status</option>
            <option value="Solved">Solved</option>
            <option value="In Progress">In Progress</option>
            <option value="Not Started">Not Started</option>
          </select>

          <select 
            value={filter.category}
            onChange={(e) => setFilter({...filter, category: e.target.value})}
          >
            <option value="All">All Categories</option>
            <option value="Array & Hashing">Array & Hashing</option>
            <option value="Two Pointers">Two Pointers</option>
            <option value="Sliding Window">Sliding Window</option>
            <option value="Stack">Stack</option>
            <option value="Binary Search">Binary Search</option>
            <option value="Linked List">Linked List</option>
            <option value="Tree">Tree</option>
            <option value="Heap & Priority Queue">Heap & Priority Queue</option>
            <option value="Backtracking">Backtracking</option>
            <option value="Tries">Tries</option>
            <option value="Graph">Graph</option>
            <option value="Dynamic Programming">Dynamic Programming</option>
            <option value="Greedy">Greedy</option>
            <option value="Intervals">Intervals</option>
            <option value="Math & Geometry">Math & Geometry</option>
            <option value="Bit Manipulation">Bit Manipulation</option>
          </select>
        </div>

        <div className="problems-list">
          {filteredProblems.map(problem => (
            <ProblemRow key={problem.id} problem={problem} />
          ))}
        </div>
      </div>
    </div>
  )
}

export default App
