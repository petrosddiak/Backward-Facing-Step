/*---------------------------------------------------------------------------*\
  =========                 |
  \\      /  F ield         | OpenFOAM: The Open Source CFD Toolbox
   \\    /   O peration     |
    \\  /    A nd           | www.openfoam.com
     \\/     M anipulation  |
-------------------------------------------------------------------------------
    Copyright (C) 2019-2021 OpenCFD Ltd.
    Copyright (C) YEAR AUTHOR, AFFILIATION
-------------------------------------------------------------------------------
License
    This file is part of OpenFOAM.

    OpenFOAM is free software: you can redistribute it and/or modify it
    under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    OpenFOAM is distributed in the hope that it will be useful, but WITHOUT
    ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
    FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License
    for more details.

    You should have received a copy of the GNU General Public License
    along with OpenFOAM.  If not, see <http://www.gnu.org/licenses/>.

\*---------------------------------------------------------------------------*/

#include "fixedValueFvPatchFieldTemplate.H"
#include "addToRunTimeSelectionTable.H"
#include "fvPatchFieldMapper.H"
#include "volFields.H"
#include "surfaceFields.H"
#include "unitConversion.H"
#include "PatchFunction1.H"

//{{{ begin codeInclude

//}}} end codeInclude


// * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * //

namespace Foam
{

// * * * * * * * * * * * * * * * Local Functions * * * * * * * * * * * * * * //

//{{{ begin localCode

//}}} end localCode


// * * * * * * * * * * * * * * * Global Functions  * * * * * * * * * * * * * //

// dynamicCode:
// SHA1 = 63e2ce7aeb855673bb82c1f10cc5d68064719d2c
//
// unique function name that can be checked if the correct library version
// has been loaded
extern "C" void powerLawProfile_63e2ce7aeb855673bb82c1f10cc5d68064719d2c(bool load)
{
    if (load)
    {
        // Code that can be explicitly executed after loading
    }
    else
    {
        // Code that can be explicitly executed before unloading
    }
}

// * * * * * * * * * * * * * * Static Data Members * * * * * * * * * * * * * //

makeRemovablePatchTypeField
(
    fvPatchVectorField,
    powerLawProfileFixedValueFvPatchVectorField
);

} // End namespace Foam


// * * * * * * * * * * * * * * * * Constructors  * * * * * * * * * * * * * * //

Foam::
powerLawProfileFixedValueFvPatchVectorField::
powerLawProfileFixedValueFvPatchVectorField
(
    const fvPatch& p,
    const DimensionedField<vector, volMesh>& iF
)
:
    parent_bctype(p, iF)
{
    if (false)
    {
        printMessage("Construct powerLawProfile : patch/DimensionedField");
    }
}


Foam::
powerLawProfileFixedValueFvPatchVectorField::
powerLawProfileFixedValueFvPatchVectorField
(
    const powerLawProfileFixedValueFvPatchVectorField& rhs,
    const fvPatch& p,
    const DimensionedField<vector, volMesh>& iF,
    const fvPatchFieldMapper& mapper
)
:
    parent_bctype(rhs, p, iF, mapper)
{
    if (false)
    {
        printMessage("Construct powerLawProfile : patch/DimensionedField/mapper");
    }
}


Foam::
powerLawProfileFixedValueFvPatchVectorField::
powerLawProfileFixedValueFvPatchVectorField
(
    const fvPatch& p,
    const DimensionedField<vector, volMesh>& iF,
    const dictionary& dict
)
:
    parent_bctype(p, iF, dict)
{
    if (false)
    {
        printMessage("Construct powerLawProfile : patch/dictionary");
    }
}


Foam::
powerLawProfileFixedValueFvPatchVectorField::
powerLawProfileFixedValueFvPatchVectorField
(
    const powerLawProfileFixedValueFvPatchVectorField& rhs
)
:
    parent_bctype(rhs),
    dictionaryContent(rhs)
{
    if (false)
    {
        printMessage("Copy construct powerLawProfile");
    }
}


Foam::
powerLawProfileFixedValueFvPatchVectorField::
powerLawProfileFixedValueFvPatchVectorField
(
    const powerLawProfileFixedValueFvPatchVectorField& rhs,
    const DimensionedField<vector, volMesh>& iF
)
:
    parent_bctype(rhs, iF)
{
    if (false)
    {
        printMessage("Construct powerLawProfile : copy/DimensionedField");
    }
}


// * * * * * * * * * * * * * * * * Destructor  * * * * * * * * * * * * * * * //

Foam::
powerLawProfileFixedValueFvPatchVectorField::
~powerLawProfileFixedValueFvPatchVectorField()
{
    if (false)
    {
        printMessage("Destroy powerLawProfile");
    }
}


// * * * * * * * * * * * * * * * Member Functions  * * * * * * * * * * * * * //

void
Foam::
powerLawProfileFixedValueFvPatchVectorField::updateCoeffs()
{
    if (this->updated())
    {
        return;
    }

    if (false)
    {
        printMessage("updateCoeffs powerLawProfile");
    }

//{{{ begin code
    #line 32 "/home/petros/cfd_projects/step_duct/0/U/boundaryField/inlet"
const scalar Uinf = 44.2;     // reference velocity
        const scalar n = 7.0;         // 1/7th power law
        const scalar delta = 0.02;    // <-- THIS is what you'll tune

        const vectorField& Cf = patch().Cf();
        vectorField& field = *this;

        // --- detect wall position automatically
        scalar yWall = GREAT;
        forAll(Cf, i)
        {
            yWall = min(yWall, Cf[i].y());
        }

        forAll(Cf, i)
        {
            scalar y = Cf[i].y();
            scalar yLocal = y - yWall;

            if (yLocal <= 0)
            {
                field[i] = vector(0,0,0);
            }
            else if (yLocal >= delta)
            {
                field[i] = vector(Uinf, 0, 0);
            }
            else
            {
                scalar U = Uinf * pow(yLocal/delta, 1.0/n);
                field[i] = vector(U, 0, 0);
            }
        }
//}}} end code

    this->parent_bctype::updateCoeffs();
}


// ************************************************************************* //

