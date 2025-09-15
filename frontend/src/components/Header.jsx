import { BlockMath } from 'react-katex';

export default function Header({ distributionName, formula }) {

    return (
        <header className="flex flex-col justify-center items-center py-3 header">
            <h1 className="text-5xl font-bold mb-2">{distributionName}</h1>
            <div className="text-xl">
                <BlockMath 
                    math={formula} 
                />
            </div>
        </header>

    );

}