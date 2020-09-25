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
		else if (this.fakeWithAncestors && !(definitionIndex in this.library))
		{
			this.cells[cellIndex] = new Plant(definitionIndex,this.nextLifeFormIndex,this.nextModelIndex);
			this.cells[cellIndex].definitionIndexShown = definitionIndexShownForParent;

			if (definitionIndex != definitionIndexShownForParent)
			{
				this.definitionIndicesWithoutModel.add(definitionIndex);
			}

			this.nextModelIndex++;
		}

		//Build from scratch
		else
		{
			this.cells[cellIndex] = new Plant(definitionIndex,this.nextLifeFormIndex,this.nextModelIndex);
			this.nextModelIndex++;
		}

		this.nextLifeFormIndex++;

		if (this.useLibrary)
		{
			this.library.add(definitionIndex);
		}
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
					if (plant.definitionIndex in this.poolPerDefinitionIndex)
					{
						this.poolPerDefinitionIndex[plant.definitionIndex].push(plant.modelIndex);
					}
					else
					{
						this.poolPerDefinitionIndex[plant.definitionIndex] = [plant.modelIndex];
					}					
				}

				this.cells[cellIndex] = null;
			}
		}

		if (this.fakeWithAncestors && this.definitionIndicesWithoutModel.length > 0)
		{
			this.library.add(this.definitionIndicesWithoutModel[Math.floor(Math.random() * this.definitionIndicesWithoutModel.length)])
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
}

// ========= only visualization below ============

function visualize_simulation(simulation,elem,name)
{
	var html = '<div class="buttonArea"><button id="'+name+'_1day"><img src="simulate_1_day_button.svg"></button><button id="'+name+'_10days"><img src="simulate_10_days_button.svg"></button><button id="'+name+'_reset"><img src="reset_button.svg"></button><button id="'+name+'_addPlant1"><img src="add_plant_1_button.svg"></button><button id="'+name+'_addPlant2"><img src="add_plant_2_button.svg"></button>';

	if (simulation.useLibrary)
	{
		html += '<button id="library"><img src="library_button.svg"></button>';
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

	update_cells(simulation,table);

	document.getElementById(name+'_1day').onclick = function()
	{
		simulation.liveADay();
		update_cells(simulation,table);
		update_pool(simulation,pool);		
		update_library(simulation,library);		
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

		update_cells(simulation,table);
		update_pool(simulation,pool);		
		update_library(simulation,library);		
	};

	document.getElementById(name+'_reset').onclick = function()
	{
		simulation.cells = [];
		update_cells(simulation,table);
		update_pool(simulation,pool);
		update_library(simulation,library);				
	};

	document.getElementById(name+'_addPlant1').onclick = function()
	{
		simulation.addPlantAtRandomLocation(1);
		update_cells(simulation,table);
		update_pool(simulation,pool);
		update_library(simulation,library);				
	};

	document.getElementById(name+'_addPlant2').onclick = function()
	{
		simulation.addPlantAtRandomLocation(2);
		update_cells(simulation,table);
		update_pool(simulation,pool);
		update_library(simulation,library);		
	};

}

function update_cells(simulation, elem)
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
				html += '<img src="plant_model_'+plant.definitionIndexShown%5+'.svg"><div class="speciesIdentifier">'+plant.definitionIndexShown+'</div><div>PLANT <span class="stress_nr">'+plant.definitionIndex+'</span></div><div>ORGANISM <span class="stress_nr">'+plant.lifeFormIndex+'</span></div><div>MODEL <span class="stress_nr">'+plant.modelIndex+'</span></div>';
			}

			html += '</td>';
		}

		html += '</tr>'
	}

	elem.innerHTML = html;

}

function update_pool(simulation,elem)
{
	var todo = -7;

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
			html+= '<img src="plant_model_'+definitionIndex%5+'.svg"><div class="speciesIdentifier">'+definitionIndex+'</div><div>MODEL <span class="stress_nr">'+model+'</span></div>';
			nr++;

			if (nr == 7)
			{
				html += '<div>'+todo+' more</div>';
				break;
			}
		}

		if (nr == 7)
		{
			break;
		}
	}

	elem.innerHTML = html;		
}

function update_library(simulation,elem)
{
	var html = '';
	var nr = 0;

	for (var definitionIndex of simulation.library)
	{
		html+= '<img src="plant_model_'+definitionIndex%5+'.svg"><div class="speciesIdentifier">'+definitionIndex+'</div>';
		nr++;

		if (nr == 7)
		{
			todo = simulation.library.length - 7;
			html += '<div>'+todo+' more</div>';
			break;
		}
	}

	elem.innerHTML = html;			
}