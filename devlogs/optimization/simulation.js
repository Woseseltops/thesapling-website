class Plant
{
	constructor(definitionIndex,lifeFormIndex,modelIndex)
	{
		this.age = 0;
		this.maximumAge = 5;
		this.spreadSeedsAtAge = 3;

		this.definitionIndex = definitionIndex;
		this.definitionIndexShown = definitionIndex;
		this.lifeFormIndex = lifeFormIndex;
		this.modelIndex = modelIndex;
	}
}

class Simulation
{
	constructor()
	{
		this.randomMutations = false;

		this.usePool = false;
		this.useLibrary = false;
		this.fakeWithAncestors = false;

		this.width = 5;
		this.height = 5;

		this.cells = [];

		this.nextLifeFormIndex = 1;
		this.nextModelIndex = 1;

		this.poolPerDefinitionIndex = {};
		this.library = new Set();

		this.definitionIndicesWithoutModel = new Set();

		for (var i = 0; i < this.width*this.height; i++)
		{
			this.cells[i] = null;
		}
	}

	addPlant(cellIndex,definitionIndex,definitionIndexShownForParent)
	{
		//First check the pool
		if (this.usePool && definitionIndex in this.poolPerDefinitionIndex && this.poolPerDefinitionIndex[definitionIndex].length > 0)
		{
			this.cells[cellIndex] = new Plant(definitionIndex,this.nextLifeFormIndex,this.poolPerDefinitionIndex[definitionIndex].pop());
		}

		//Use an ancestor
		else if (this.fakeWithAncestors && !this.library.has(definitionIndex))
		{
			//First check the pool 
			if (definitionIndexShownForParent in this.poolPerDefinitionIndex && this.poolPerDefinitionIndex[definitionIndexShownForParent].length > 0)
			{
				this.cells[cellIndex] = new Plant(definitionIndex,this.nextLifeFormIndex,this.poolPerDefinitionIndex[definitionIndexShownForParent].pop());
			}
			//Else, copy from the library
			else
			{
				this.cells[cellIndex] = new Plant(definitionIndex,this.nextLifeFormIndex,this.nextModelIndex);
				this.nextModelIndex++;
			}

			this.cells[cellIndex].definitionIndexShown = definitionIndexShownForParent;

			if (definitionIndex != definitionIndexShownForParent)
			{
				this.definitionIndicesWithoutModel.add(definitionIndex);
			}
		}

		//Build from scratch or copy from the library
		else
		{
			this.cells[cellIndex] = new Plant(definitionIndex,this.nextLifeFormIndex,this.nextModelIndex);
			this.nextModelIndex++;
		}

		if (this.useLibrary)
		{
			this.library.add(this.cells[cellIndex].definitionIndexShown);
		}

		this.nextLifeFormIndex++;
	}

	addPlantAtRandomLocation(definitionIndex)
	{
		this.addPlant(Math.floor(Math.random() * this.width * this.height),definitionIndex,definitionIndex);
	}

	liveADay()
	{
		for (var cellIndex in this.cells)
		{
			var plant = this.cells[cellIndex];

			if (plant == null)
			{
				continue;
			} 

			plant.age++;

			if (plant.age == plant.spreadSeedsAtAge)
			{
				var firstCellNextTo = this.getRandomCellNextTo(cellIndex);
				var secondCellNextTo = this.getRandomCellNextTo(cellIndex);

				var definitionIndex;

				if (this.cells[firstCellNextTo] == null)
				{
					definitionIndex = plant.definitionIndex;

					if (this.randomMutations && Math.random() > 0.7)
					{
						definitionIndex += 1;
					}

					this.addPlant(firstCellNextTo,definitionIndex,plant.definitionIndexShown);
				}

				if (this.cells[secondCellNextTo] == null)
				{
					definitionIndex = plant.definitionIndex;

					if (this.randomMutations && Math.random() > 0.7)
					{
						definitionIndex += 1;
					}

					this.addPlant(secondCellNextTo,definitionIndex,plant.definitionIndexShown);
				}
			}
			else if (plant.age == plant.maximumAge)
			{
				if (this.usePool)
				{
					if (plant.definitionIndexShown in this.poolPerDefinitionIndex)
					{
						this.poolPerDefinitionIndex[plant.definitionIndexShown].push(plant.modelIndex);
					}
					else
					{
						this.poolPerDefinitionIndex[plant.definitionIndexShown] = [plant.modelIndex];
					}					
				}

				this.cells[cellIndex] = null;
			}
		}

		this.definitionIndicesWithoutModel = new Set();
	}

	getRandomCellNextTo(cellIndex)
	{
		var coordinates = this.cellIndexToCoordinates(cellIndex);
		var x = coordinates[0];
		var y = coordinates[1];

		var options = [[x-1,y-1],[x-1,y],[x-1,y+1],
						[x,y-1], [x,y+1],
						[x+1,y-1],[x+1,y],[x+1,y+1]];

		var chosenCell = options[Math.floor(Math.random() * options.length)];

		if (chosenCell[0] < 0)
		{
			chosenCell[0] = 0;
		}
		else if (chosenCell[0] >= this.width)
		{
			chosenCell[0] = this.width-1;
		}

		if (chosenCell[1] < 0)
		{
			chosenCell[1] = 0;
		}
		else if (chosenCell[1] >= this.width)
		{
			chosenCell[1] = this.width-1;
		}

		return this.coordinatesToCellIndex(chosenCell[0],chosenCell[1]);
	}

	cellIndexToCoordinates(cellIndex)
	{
		var x = cellIndex%this.width;
		var y = Math.floor(cellIndex/this.height);

		return [x,y];
	}

	coordinatesToCellIndex(x, y)
	{
		return this.height*y + x;
	}

	addModelToLibrary()
	{
		var newModelIndex = 1;

		while (true)
		{
			if (!this.library.has(newModelIndex))
			{
				this.library.add(newModelIndex);
				break;
			}

			newModelIndex++;
		}
	}
}

// ========= only visualization below ============

function visualize_simulation(simulation,elem,name,prefix)
{
	var html = '<div class="buttonArea"><button id="'+name+'_1day"><img src="'+prefix+'simulate_1_day_button.svg"></button><button id="'+name+'_10days"><img src="'+prefix+'simulate_10_days_button.svg"></button><button id="'+name+'_reset"><img src="'+prefix+'reset_button.svg"></button><button id="'+name+'_addPlant1"><img src="'+prefix+'add_plant_1_button.svg"></button><button id="'+name+'_addPlant2"><img src="'+prefix+'add_plant_2_button.svg"></button>';

	if (simulation.randomMutations)
	{
		html += '<button id="'+name+'_addToLibrary"><img src="'+prefix+'library_button.svg"></button>';
	}

	html += '</div><table id="'+name+'_table"></table>';

	if (simulation.usePool)
	{
		html += '<div class="pool" id="'+name+'_pool"></div>';
	}

	if (simulation.useLibrary)
	{
		html += '<div class="library" id="'+name+'_library"></div>';
	}
	elem.innerHTML = html;

	var table = document.getElementById(name+'_table');
	var pool = document.getElementById(name+'_pool');
	var library = document.getElementById(name+'_library');

	update_cells(simulation,table,prefix);

	document.getElementById(name+'_1day').onclick = function()
	{
		simulation.liveADay();
		update_cells(simulation,table,prefix);
		update_pool(simulation,pool,prefix);		
		update_library(simulation,library,prefix);		
	};

	document.getElementById(name+'_10days').onclick = function()
	{
		simulation.liveADay();
		simulation.liveADay();
		simulation.liveADay();
		simulation.liveADay();
		simulation.liveADay();

		simulation.liveADay();
		simulation.liveADay();
		simulation.liveADay();
		simulation.liveADay();
		simulation.liveADay();

		update_cells(simulation,table,prefix);
		update_pool(simulation,pool,prefix);		
		update_library(simulation,library,prefix);		
	};

	document.getElementById(name+'_reset').onclick = function()
	{
		simulation.cells = [];
		simulation.poolPerDefinitionIndex = {};
		simulation.library = new Set();

		simulation.nextLifeFormIndex = 1;
		simulation.nextModelIndex = 1;

		update_cells(simulation,table,prefix);
		update_pool(simulation,pool,prefix);
		update_library(simulation,library,prefix);				
	};

	document.getElementById(name+'_addPlant1').onclick = function()
	{
		simulation.addPlantAtRandomLocation(1);
		update_cells(simulation,table,prefix);
		update_pool(simulation,pool,prefix);
		update_library(simulation,library,prefix);				
	};

	document.getElementById(name+'_addPlant2').onclick = function()
	{
		simulation.addPlantAtRandomLocation(2);
		update_cells(simulation,table,prefix);
		update_pool(simulation,pool,prefix);
		update_library(simulation,library,prefix);		
	};

	if (simulation.randomMutations)
	{
		document.getElementById(name+'_addToLibrary').onclick = function()
		{
			simulation.addModelToLibrary();
			update_library(simulation,library,prefix);
		};		
	}
}

function update_cells(simulation, elem, prefix)
{
	var cellIndex;
	var html = '';

	for (var y = 0; y < simulation.height; y++)
	{
		html += '<tr>'

		for (var x = 0; x < simulation.width; x++)
		{
			cellIndex = y*simulation.width + x;

			html += '<td>';

			plant = simulation.cells[cellIndex];

			if (plant != null)
			{
				html += '<img src="'+prefix+'plant_model_'+plant.definitionIndexShown%5+'.svg"><div class="speciesIdentifier">'+plant.definitionIndexShown+'</div><div ';

				if (plant.definitionIndex != plant.definitionIndexShown)
				{
					html += 'class="showing_fake"';
				}

				html += '>SPECIES <span class="stress_nr">'+plant.definitionIndex+'</span></div><div>ORGANISM <span class="stress_nr">'+plant.lifeFormIndex+'</span></div><div>MODEL <span class="stress_nr">'+plant.modelIndex+'</span></div>';
			}

			html += '</td>';
		}

		html += '</tr>'
	}

	elem.innerHTML = html;

}

function update_pool(simulation,elem,prefix)
{
	if (elem == null)
	{
		return;
	}

	var maxNumberOfItems = 11;

	var todo = -maxNumberOfItems;

	for (var [definitionIndex,pool] of Object.entries(simulation.poolPerDefinitionIndex))
	{
		todo += pool.length;
	}

	var html = '';
	var nr = 0;

	for (var [definitionIndex,pool] of Object.entries(simulation.poolPerDefinitionIndex))
	{
		for (var model of pool)
		{
			html+= '<img src="'+prefix+'plant_model_'+definitionIndex%5+'.svg"><div class="speciesIdentifier">'+definitionIndex+'</div><div>MODEL <span class="stress_nr">'+model+'</span></div>';
			nr++;

			if (nr == maxNumberOfItems)
			{
				html += '<div class="not_shown_plants">'+todo+' more</div>';
				break;
			}
		}

		if (nr == maxNumberOfItems)
		{
			break;
		}
	}

	elem.innerHTML = html;		
}

function update_library(simulation,elem,prefix)
{	
	if (elem == null)
	{
		return;
	}

	var maxNumberOfItems = 15;

	var html = '';
	var nr = 0;

	for (var definitionIndex of simulation.library)
	{
		html+= '<img src="'+prefix+'plant_model_'+definitionIndex%5+'.svg"><div class="speciesIdentifier">'+definitionIndex+'</div>';
		nr++;

		if (nr == maxNumberOfItems)
		{
			todo = simulation.library.size - maxNumberOfItems;
			html += '<div>'+todo+' more</div>';
			break;
		}
	}

	elem.innerHTML = html;			
}