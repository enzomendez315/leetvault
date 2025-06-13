import type { Problem } from '../types/Problem';
import './ProblemRow.css';

interface ProblemRowProps {
    problem: Problem;
}

function ProblemRow({ problem }: ProblemRowProps) {
    const getDifficultyColor = (difficulty: string) => {
        switch (difficulty) {
            case 'Easy': return '#00b8a3';
            case 'Medium': return '#ffc01e';
            case 'Hard': return '#ff375f';
            default: return '#000000';
        }
    };

    return (
        <div className="problem-row">
            <div className="problem-header">
                <span className="problem-number">#{problem.number}</span>
                <h3 className="problem-name">{problem.name}</h3>
                <span 
                    className="problem-difficulty"
                    style={{ color: getDifficultyColor(problem.difficulty) }}
                >
                    {problem.difficulty}
                </span>
            </div>
            <div className="problem-details">
                <p className="problem-description">{problem.description}</p>
                <div className="problem-meta">
                    <span className="problem-category">{problem.category}</span>
                    <span className="problem-complexity">
                        Time: {problem.timeComplexity} | Space: {problem.spaceComplexity}
                    </span>
                </div>
                <div className="problem-status">
                    <span className={`status-badge ${problem.status.toLowerCase().replace(' ', '-')}`}>
                        {problem.status}
                    </span>
                    <span className="date-solved">Solved: {problem.dateSolved}</span>
                </div>
            </div>
        </div>
    );
}

export default ProblemRow; 