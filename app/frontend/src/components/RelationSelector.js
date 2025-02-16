import React, { useState, useEffect } from 'react'
import { useDispatch, useSelector } from 'react-redux'
import { makeId, formatStructuredName } from '../utilities'
import { addRel, deleteRel } from '../store/relations/actions'
import { BelongsToSelector } from './BelongsToSelector'
import { Relation } from './Relation'

export const RelationSelector = () => {
	const dispatch = useDispatch()
	const [structuredNames, relations] = useSelector(state => [
		state.selectedStructuredNames
			.map(v => {
				return {
					id: v,
					formattedName: formatStructuredName(state.map[v], state),
				}
			})
			.sort((a, b) => {
				if (a.id === b.id) {
					return 0
				}

				return a.id < b.id ? -1 : 1
			}),
		state.rel.map(v => {
			return { ...v }
		}),
	])

	const [primaryName, setPrimaryName] = useState(-1)

	useEffect(() => {
		if (!structuredNames.find(v => v.id === primaryName)) {
			if (structuredNames.length === 0) setPrimaryName(-1)
			else setPrimaryName(structuredNames[0].id)
		}
	}, [structuredNames])

	const match = (rel, idA, idB) =>
		(rel.name1 === idA && rel.name2 === idB) ||
		(rel.name1 === idB && rel.name2 === idA)

	const relationExists = (idA, idB) => relations.find(v => match(v, idA, idB))

	const toggleRelation = (idA, idB) => {
		if (relationExists(idA, idB)) {
			relations.find(v =>
				match(v, idA, idB) ? dispatch(deleteRel(v)) || true : false
			)
		} else {
			dispatch(
				addRel({
					id: makeId('relation'),
					name1: idA,
					name2: idB,
					belongs_to: 0,
					reference_id: -1,
				})
			)
		}
	}

	return (
		<>
			<h2>Create relations</h2>
			<div id='relation-selector'>
				<div>
					{structuredNames.map(v => (
						<div
							key={v.id}
							className={`w3-btn ${
								v.id === primaryName ? 'w3-green' : ''
							}`}
							onClick={() => setPrimaryName(v.id)}
						>
							{v.formattedName}
						</div>
					))}
				</div>

				<div>
					{structuredNames
						.filter(v => v.id !== primaryName)
						.map(v => (
							<div
								key={v.id}
								className={`w3-btn ${
									relationExists(primaryName, v.id)
										? 'w3-green'
										: ''
								}`}
								onClick={() =>
									toggleRelation(primaryName, v.id)
								}
							>
								<BelongsToSelector
									idA={primaryName}
									idB={v.id}
									relation={relationExists(primaryName, v.id)}
								/>
								{v.formattedName}
							</div>
						))}
				</div>
			</div>
			<div>
				<h3>Relations</h3>
				<table>
					<thead>
						<tr>
							<th>Structured Name 1</th>
							<th>Swap</th>
							<th>Belongs To</th>
							<th>Structured Name 2</th>
						</tr>
					</thead>
					<tbody>
						{relations.map(v => (
							<Relation key={v.id} relation={v} />
						))}
					</tbody>
				</table>
			</div>
		</>
	)
}
